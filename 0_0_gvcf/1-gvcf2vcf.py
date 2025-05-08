#!/usr/bin/env python3
"""
Convert gVCF files in a flat directory into single‑sample, per‑site VCFs.

変更点の概要（以前のバージョンからの主な違い）
--------------------------------------------------
* **入力ディレクトリ固定**:  /home/mkato/hdd_data/0_0_gvcf/
* **出力ディレクトリ固定**: /home/mkato/hdd_data/0_1_vcf/
* サンプルごとのサブディレクトリを廃止し、元ファイル名をそのまま利用
* YAML 設定は任意。無ければデフォルトを適用
* argparse／logging を導入し、CLI とログの見通しを向上
* Pathlib + concurrent.futures で可読性を確保

このスクリプトは「あとから読んでも処理の流れを追いやすい」ことを目標に、
要所に **日本語コメント** を付加しています。
"""
from __future__ import annotations

# ===== 標準ライブラリ =====
import argparse
import gzip
import logging
import os
import re
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List
from itertools import chain

# ===== 外部ライブラリ（オプション） =====
# YAML ファイルで設定を読み込む場合のみ必要。
try:
    import yaml  # type: ignore
except ImportError:
    yaml = None  # PyYAML が無い場合は None を設定し、後段で判定

################################################################################
# 1. デフォルト設定
################################################################################
#   YAML が無い場合のフォールバックとして使われる。
#   必要があれば CLI で上書き可能。
################################################################################
DEFAULT_CFG: Dict[str, Any] = {
    "input_dir": "/home/mkato/hdd_data/0_0_gvcf/",   # gVCF の格納先
    "output_dir": "/home/mkato/hdd_data/0_1_vcf/",  # 変換後 VCF の出力先
    "threads": os.cpu_count() or 4,                    # 並列ジョブ数
    "filter_depth": 3,                               # DP のフィルタ閾値
    "options": {
        "remove_chr_prefix": True,  # 'chr' を削除
        "remove_non_ref": True,     # ALT の <NON_REF> を除去
        "assign_id": True,          # CHROM:POS を ID に設定
        "expand_end": True,         # END=xxx を 1 bp ずつ展開
    },
}

################################################################################
# 2. 補助関数
################################################################################

def load_config(path: str | None) -> Dict[str, Any]:
    """YAML から設定を読み込んでデフォルトとマージする関数。"""
    if path is None:
        return DEFAULT_CFG

    if yaml is None:
        logging.error("PyYAML がインストールされていないため %s を読み込めません", path)
        sys.exit(1)

    cfg_path = Path(path).expanduser().resolve()
    with cfg_path.open() as fh:
        cfg: Dict[str, Any] = yaml.safe_load(fh)

    # デフォルト設定に読み込んだ値を上書き
    merged = {**DEFAULT_CFG, **cfg}
    # options はネストしているので個別にマージ
    merged.setdefault("options", {}).update(cfg.get("options", {}))
    return merged


def ensure_output_dir(path: Path) -> None:
    """出力ディレクトリが無ければ作成するユーティリティ関数。"""
    path.mkdir(parents=True, exist_ok=True)

################################################################################
# 3. gVCF → VCF 変換のメインロジック
################################################################################

def process_vcf(
    input_path: Path,
    output_path: Path,
    options: Dict[str, bool],
    filter_depth: int,
) -> None:
    """1 つの gVCF を読み込み、条件を満たすレコードを VCF に書き出す。"""

    logging.debug("Processing %s -> %s", input_path.name, output_path.name)

    # gzip.open(..., "rt") でテキストモード読み取り／書き込み
    with gzip.open(input_path, "rt") as infile, gzip.open(output_path, "wt") as outfile:
        for line in infile:
            # -------------------- ヘッダ行の処理 --------------------
            if line.startswith("#"):
                if options.get("remove_chr_prefix") and (
                    line.startswith("##contig") or line.startswith("#CHROM")
                ):
                    # 例: ##contig=<ID:chr1,length=...> → ##contig=<ID:1,length=...>
                    line = re.sub(r"chr(\d+)", r"\1", line)
                outfile.write(line)
                continue  # ヘッダはここで完了

            # -------------------- データ行の処理 --------------------
            # gVCF は <NON_REF> を ALT に含む "block" 行が混在する
            fields: List[str] = line.rstrip("\n").split("\t")
            chrom, pos, _id, ref, alt, qual, flt, info, fmt, sample = fields[:10]

            # (1) CHROM の 'chr' プレフィックスを削除
            if options.get("remove_chr_prefix"):
                chrom = re.sub(r"^chr", "", chrom)
                fields[0] = chrom

            # (2) ALT の <NON_REF> を削除／置換
            if options.get("remove_non_ref"):
                alt = re.sub(r",<NON_REF>", "", alt)  # 変異 + <NON_REF> の場合
                alt = re.sub(r"^<NON_REF>$", ".", alt)  # 非変異ブロックのみの場合
                fields[4] = alt

            # (3) DP と GT の列番号を取得
            fmt_fields = fmt.split(":")
            dp_idx = fmt_fields.index("DP") if "DP" in fmt_fields else -1
            gt_idx = fmt_fields.index("GT") if "GT" in fmt_fields else -1
            if dp_idx == -1 or gt_idx == -1:
                continue  # 必要な情報が無ければスキップ

            # サンプルフィールドを ':' で分割し、深さとジェノタイプを抽出
            samp_fields = sample.split(":")
            try:
                depth = int(samp_fields[dp_idx])
            except (ValueError, IndexError):
                depth = 0  # 欠損や不適切な値は深さ 0 とみなす
            genotype = samp_fields[gt_idx] if gt_idx < len(samp_fields) else "./."

            # (4) DP と GT によるフィルタリング
            if depth < filter_depth or genotype == "./.":
                continue  # 条件を満たさない行はここで終了

            # (5) ID フィールドを CHROM:POS に更新
            if options.get("assign_id"):
                fields[2] = f"{chrom}:{pos}"

            # (6) END ブロックを 1bp 解像度に展開
            if options.get("expand_end") and (m := re.search(r"END=(\d+)", info)):
                end_pos = int(m.group(1))
                for new_pos in range(int(pos), end_pos + 1):
                    fields[1] = str(new_pos)  # POS を更新
                    if options.get("assign_id"):
                        fields[2] = f"{chrom}:{new_pos}"

                    # ブロック内の後続サイトは非変異なので簡易的なフィールドに置換
                    if new_pos != int(pos):
                        fields[3:8] = [".", ".", ".", ".", f"DP={depth}"]
                    outfile.write("\t".join(fields) + "\n")
            else:
                outfile.write("\t".join(fields) + "\n")

################################################################################
# 4. スクリプトのエントリポイント
################################################################################

def main(argv: List[str] | None = None) -> None:
    """コマンドライン引数を解析し、並列で gVCF を処理するメイン関数。"""

    # -------------------- CLI 定義 --------------------
    parser = argparse.ArgumentParser(
        description="Convert gVCF files under input_dir to single-sample per-site VCFs"
    )
    parser.add_argument("--config", help="YAML config file", default=None)
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Print debug information"
    )
    args = parser.parse_args(argv)

    # -------------------- ログ設定 --------------------
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    # -------------------- 設定読み込み --------------------
    cfg = load_config(args.config)
    input_dir = Path(cfg["input_dir"]).expanduser().resolve()
    output_dir = Path(cfg["output_dir"]).expanduser().resolve()
    threads = int(cfg["threads"])

    ensure_output_dir(output_dir)

    # -------------------- 入力ファイル探索 --------------------
    # .vcf.gz と .gvcf.gz の両方を対象にする
    vcf_files = list(chain(
        input_dir.glob("*.vcf.gz"),
        input_dir.glob("*.gvcf.gz")
    ))

    # ファイルかどうかをチェック
    vcf_files = [p for p in vcf_files if p.is_file()]
    logging.info("%d gVCF ファイルを検出", len(vcf_files))
    if not vcf_files:
        logging.warning("入力ディレクトリ %s に *.vcf.gz が見つかりません", input_dir)
        return

    options: Dict[str, bool] = cfg.get("options", {})
    fdepth: int = int(cfg.get("filter_depth", 0))

    # -------------------- 並列処理 --------------------
    with ProcessPoolExecutor(max_workers=threads) as pool:
        futures = {
            pool.submit(
                process_vcf,
                inp,
                output_dir / inp.name,
                options,
                fdepth,
            ): inp.name
            for inp in vcf_files
        }

        # 完了を逐次チェックしてログを出力
        for fut in as_completed(futures):
            name = futures[fut]
            try:
                fut.result()
                logging.info("✔ Finished %s", name)
            except Exception as exc:  # pylint: disable=broad-except
                logging.exception("✖ Error processing %s: %s", name, exc)


# -----------------------------------------------------------------------------
# Python スクリプトとして実行された場合だけ main() を呼び出す
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
