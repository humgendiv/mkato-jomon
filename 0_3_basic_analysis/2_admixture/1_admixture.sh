#!/bin/bash
# Admixture解析スクリプト（LD pruning + K=2〜10のCV付きアダプチャー）

# 入力PLINKプレフィックス
INPUT_PREFIX="/home/mkato/hdd_data/0_3_basic_analysis/2_admixture/merged_with_1240K.targetpops"
# LDプルーニング後の出力プレフィックス
PRUNED_PREFIX="${INPUT_PREFIX}.pruned"
# 実行するKの範囲
KMIN=2
KMAX=5

# 出力ディレクトリ（任意）
OUTDIR="/home/mkato/hdd_data/0_3_basic_analysis/2_admixture"

mkdir -p "$OUTDIR"

# ステップ1: LD pruning
echo "[LD PRUNE] Start LD pruning"
plink \
  --bfile "$INPUT_PREFIX" \
  --indep-pairwise 200 25 0.2 \
  --out "$PRUNED_PREFIX"

# ステップ2: Prunedデータセット作成
echo "[MAKE PRUNED BED] Extract pruned SNPs"
plink \
  --bfile "$INPUT_PREFIX" \
  --extract "${PRUNED_PREFIX}.prune.in" \
  --make-bed \
  --out "$PRUNED_PREFIX"

# ステップ3: Admixture解析（CV付き）
echo "[ADMIXTURE] Running admixture for K=$KMIN..$KMAX"
for K in $(seq $KMIN $KMAX); do
  (
    echo "[K=$K] Start"
    admixture --cv=10 -j8 \
      "${PRUNED_PREFIX}.bed" $K \
      | tee "$OUTDIR/admixture_K${K}.log"
    echo "[K=$K] Completed"
  ) &
done
wait


# ステップ4: CV error summary
echo "# K  CV_error" > "$OUTDIR/cv_errors.txt"
for K in $(seq $KMIN $KMAX); do
  CV=$(grep -h "CV error" "$OUTDIR/admixture_K${K}.log" | awk -F': ' '{print $2}')
  echo "$K  $CV" >> "$OUTDIR/cv_errors.txt"
done

echo "[DONE] Admixture analysis complete. Results in $OUTDIR"
