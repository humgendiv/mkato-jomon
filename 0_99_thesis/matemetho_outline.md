# 縄文人論文 Materials & Methods アウトライン

## 結果セクションの修正案（解釈的記述の削除）

### 3.1の修正例
**現在：**
"These findings are consistent with previous studies suggesting long-term genetic isolation of the Jomon population, and further demonstrate their genetic homogeneity across both time and space."

**修正案：**
"All eight high-coverage Jomon individuals derived >95% of their ancestry from a single genetic component (green), with continental East Asian contributions consistently below 5%."

### 3.2の修正例
**現在：**
"This parallel pattern across Jomon samples suggests that the observed geographic variation reflects the population structure of modern Japanese..."

**修正案：**
"All Jomon samples showed the lowest f₃ values with Kinki populations (0.0955-0.110) and progressively higher values toward peripheral regions, with Iyai individuals consistently exhibiting 8-10% lower absolute values than other Jomon samples."

### 3.3の修正例
**現在：**
"These results suggest that Initial Jomon populations underwent subtle genetic changes between the Initial and Early periods..."

**修正案：**
"Modern Japanese showed significantly higher genetic affinity to Todoroki (Z = 3.001) and Chidorigakubo (Z = 3.199) than to Iyai individuals, while comparisons among non-Iyai Jomon groups yielded |Z| < 1."

### 3.4の修正例
**現在：**
"These patterns may reflect local adaptation to varying sodium availability..."

**修正案：**
"Iyai individuals exhibited higher cardiovascular risk scores (log₂ FC = 0.15-0.22) and lower kidney function scores (log₂ FC = -0.18) compared to coastal Jomon populations."

---

## 2. Materials & Methods

### 2.1 Sample information and data generation
**段落の役割：** 使用したサンプルの詳細情報と新規シーケンスデータの生成方法を記載

**主要内容：**
- 8個体の縄文人サンプル詳細
  - 既報2個体：F23 (Funadomari, Late Jomon, Hokkaido), I1 (Iyai, Initial Jomon, Gunma)
  - 新規6個体：T5 (Todoroki, Early Jomon, Kumamoto), I4/I15/I18 (Iyai, Initial Jomon, Gunma), M3 (Mitsusawa, Middle Jomon, 4450 cal BP, Kanagawa), C3 (Chidorigakubo, Middle Jomon, 5048 cal BP, Kanagawa)
- **【要確認】** 年代測定の詳細結果（T5の年代値）
- **【要確認】** DNA抽出・ライブラリ作成の具体的プロトコル
- **【要確認】** カバレッジ情報（共同研究先への問い合わせ必要）
- **【要確認】** 品質管理基準（mapDamage結果、contamination推定値など）

### 2.2 Reference datasets and data processing
**段落の役割：** 比較に使用した参照データセットと前処理方法を記載

**主要内容：**
- 1240K Allen Ancient DNA Resource (v54.1)
  - 330 East Asian individuals
  - 973,002 SNPs
- 現代日本人データ：47都道府県11,069人（各県50個体ランダム抽出）
  - Shimizu et al. 2024 "Prefecture-level population structure of the Japanese based on SNP genotypes of 11,069 individuals"より供与
- 低カバレッジ縄文人18個体（AADR）
- データマージ：mergeit使用
- 低カバレッジサンプルは1240Kデータセット内で特別な前処理なし

### 2.3 Population genetic analyses

#### 2.3.1 Principal Component Analysis
- smartpca (EIGENSOFT v7.2.1)使用
- パラメータ設定：lsqproject: YES, numoutlieriter: 0, altnormstyle: NO, numoutevec: 20, outliermode: 0, outliersigmathresh: 6.0
- 973,002 SNPs使用
- PC計算に使用：1240K東アジア現代人集団＋朝鮮半島・日本列島古代人集団

#### 2.3.2 ADMIXTURE analysis
- ADMIXTURE v1.3.0使用
- K=2-10でCross-validation実施（--cv=10）
- 最適K値の決定基準（CV error = 0.47379 at K=4）
- 10回の独立ラン実施
- LDプルーニング：PLINK --indep-pairwise 200 25 0.2

#### 2.3.3 f-statistics
- ADMIXTOOLS2使用
- Outgroup f₃: f₃(Mbuti; X, Y)形式
- f₄統計量: f₄(Mbuti, Test; Jomon1, Jomon2)形式
- 集団アリル頻度の計算方法（Iyai 4個体プール等）
- Block jackknife法によるエラー推定（qpf3: 714 blocks）
- 都道府県別f₃解析は独自実装のため詳細はSupplementaryへ

#### 2.3.4 f₄-ratio analysis
- qpF4ratio v400プログラム使用
- モデル設定：a=Dai, b=Korean/Han, x=Japanese, c=Jomon sources, o=Mbuti
  - Dai使用は先行研究（Adachi et al. 2021）に準拠
- 418,449-601,334 SNPs使用（サンプル依存）

### 2.4 Phylogenetic analysis
**段落の役割：** 系統解析の手法を記載

**主要内容：**
- TreeMix v1.13使用
- コマンド：treemix -i INPUT -o OUTPUT -root Mbuti -bootstrap -k 500 -noss
- Migration edge解析は今回実施せず
- Bootstrap: 500回
- Drift parameter算出

### 2.5 Polygenic risk score analysis
**段落の役割：** 表現型予測のためのPRS計算方法を記載

**主要内容：**
- Biobank Japan (BBJ) Jenger database使用
  - URL: http://jenger.riken.jp/result
- P値閾値：0.01, 0.001, 0.0001
- アリル頻度計算：Iyai 4個体プール vs その他縄文人4個体プール
- BETA値との積和計算
- 現代日本人との差分表示方法
- Log₂ fold change計算
- **【要持ち帰り】** 使用形質リストと引用文献（Supplementaryで提示予定）
- LDプルーニング・クランピングは未実施

### 2.6 Statistical analyses
**段落の役割：** 統計解析全般の方法を記載

**主要内容：**
- 有意性判定基準（|Z| > 3）
- 多重検定補正：未実施
- 使用ソフトウェアとバージョン情報のまとめ
- 図表作成：Python（解析ツール付属のプロットを除く）

---

## 調査・確認が必要な項目のまとめ

### 高優先度（共同研究者への確認が必要）
1. **カバレッジ情報** - 全サンプルの平均カバレッジ
2. **年代測定結果** - T5、I4、I15、I18の正確な年代値
3. **DNA実験の詳細** - 抽出からシーケンスまでのプロトコル
4. **品質管理データ** - contamination推定値、damage patterns

### 中優先度（解析補足情報）
5. **都道府県別f₃解析** - 独自実装の詳細（Supplementaryで記載予定）
6. **PRS解析** - 使用形質リストと引用文献（Supplementaryで提示予定）

### 記載レベルについて
参考論文（Doigahama論文）の記載レベルに準拠し、過度に詳細な技術的情報は避ける。
再現性に必要な基本的情報（ソフトウェア、主要パラメータ）に焦点を当てる。