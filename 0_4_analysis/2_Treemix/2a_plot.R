#!/usr/bin/env Rscript

# plot_treemix_tree.R
# Usage:
#   chmod +x plot_treemix_tree.R
#   ./plot_treemix_tree.R <prefix> <path/to/plotting_funcs.R> [output.pdf]

args <- commandArgs(trailingOnly = TRUE)
if(length(args) < 2) {
  cat("Usage: plot_treemix_tree.R <prefix> <plotting_funcs.R path> [output.pdf]\n")
  quit(status = 1)
}

prefix      <- args[1]
funcs_path  <- args[2]
output_file <- if(length(args) >= 3) args[3] else paste0(prefix, ".treemix.tree.pdf")

# 必要パッケージの確認・読み込み
required <- c("R.utils", "RColorBrewer")
for(pkg in required) {
  if(!require(pkg, character.only = TRUE, quietly = TRUE)) {
    install.packages(pkg, repos = "https://cloud.r-project.org")
    library(pkg, character.only = TRUE)
  }
}

# Treemix の描画関数を読み込む
source(funcs_path)

# PDF デバイスを開いてプロット
pdf(output_file, width = 7, height = 5)
# plot_tree は第一引数に prefix を取り、root は既にファイルに反映されているため不要
plot_tree(prefix, cex = 0.8)
dev.off()

cat("Saved Treemix tree plot to", output_file, "\n")
