#!/usr/bin/env python3

import sys
import gzip


def main():
    # 引数のチェック
    if len(sys.argv) != 3:
        print("Usage: plink2treemix.py [gzipped input file] [gzipped output file]", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    pop2rs = {}
    rss = []
    rss2 = set()

    # 入力ファイルをテキストモードで読み込み
    with gzip.open(input_path, 'rt') as infile:
        # ヘッダー行をスキップ
        header = infile.readline()
        for line in infile:
            parts = line.strip().split()
            # ヘッダー再出現や不正行をスキップ
            if len(parts) < 8 or parts[0] == 'CHR':
                continue

            rs = parts[1]
            pop = parts[2]
            mc = parts[6]
            total = parts[7]

            # SNPリストを保持
            if rs not in rss2:
                rss.append(rs)
                rss2.add(rs)

            # 集団ごとの辞書に追加
            if pop not in pop2rs:
                pop2rs[pop] = {}
            if rs not in pop2rs[pop]:
                pop2rs[pop][rs] = f"{mc} {total}"

    # 集団名をソートしてヘッダー出力用に取得
    pops = sorted(pop2rs.keys())

    # 出力ファイルをテキストモードで書き込み
    with gzip.open(output_path, 'wt') as outfile:
        # ヘッダー行：集団名をスペース区切りで
        print(' '.join(pops), file=outfile)

        # 各SNPについてアレルカウントを出力
        for rs in rss:
            entries = []
            for pop in pops:
                if rs in pop2rs[pop]:
                    mc_str, total_str = pop2rs[pop][rs].split()
                    c1 = int(mc_str)
                    c2 = int(total_str)
                    c3 = c2 - c1
                else:
                    # 欠損した集団は0で埋める
                    c1, c3 = 0, 0
                entries.append(f"{c1},{c3}")
            print(' '.join(entries), file=outfile)


if __name__ == '__main__':
    main()
