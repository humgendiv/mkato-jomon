# Results セクション アウトライン

## セクション全体の目的
- 縄文人8個体（既報2個体、新規6個体）の遺伝的均質性と時代的変化を明らかにする
- 現代日本人集団との遺伝的関係を定量的に評価する
- 縄文早期（居家以I1, I4, I15, I18）と前期〜後期の集団間の遺伝的差異の内容を明らかにする

---

## 3.1 縄文人集団の遺伝的構造と東アジア集団における位置づけ

### Figure 1: PCA プロット
- **段落の役割**: 縄文人集団の遺伝的均質性を示し、東アジア集団における独自性を確立
- **主要な観察結果**: 
  - 縄文人8個体が極めて緊密なクラスターを形成（PC1: ~0.01, PC2: ~0.11）
  - 現代東アジア集団から明確に分離（PC2軸で大きく離れる）
  - 過去に報告された高カバレッジでない縄文人個体の形成するクラスターに対して、高カバレッジな縄文人サンプル８個体はより密に分布
- **重要な詳細**:
  - 使用データ: 1240K Allen Ancient DNA Resource由来の330個体、973,002 SNPs
  - 8個体の縄文人とは別に、18個体の低カバレッジ縄文人サンプルがAADRに含まれることに注意。
- **次の段落への接続**: PCAで示された遺伝的独自性をADMIXTURE解析で確認

### Figure 2a-d: ADMIXTURE解析（K=3）
- **段落の役割**: 縄文人集団における大陸由来成分の欠如を確認し、先行研究（要出典）を支持
- **主要な観察結果**:
  - 縄文人は単一の遺伝的成分（緑色）でほぼ100%構成
  - 現代日本人は縄文人成分（緑）、大陸成分（青・オレンジ）の混合
- **重要な詳細**:
  - 最適K値の決定根拠（CV error）
- **次の段落への接続**: 縄文人集団内の微細な遺伝的差異を検出するためf統計量の算出による比較を行う

---

## 3.2 f統計量による縄文人集団内の微細な遺伝的差異の検出

### Figure 3: Outgroup f3 ヒートマップ
- **段落の役割**: 縄文人集団内の遺伝的距離を定量化し、時代的差異を明らかにする
- **主要な観察結果**:
  - 居家以遺跡個体（Iyai、4個体プール）と他の縄文人の間：f3 = 0.641-0.649（±0.005）
  - 居家以以外の縄文人サンプル間：f3 = 0.664-0.670（±0.006）
  - 一貫して縄文人早期集団と縄文人前期～後期集団の間の僅かな遺伝的距離が観察される
  - 現代日本人・韓国人は縄文人より明確に低い値（<0.4）
- **重要な詳細**:
  - 集団アリル頻度を使用（1個体の集団はそのまま用いる）
  - 全てのZ値 > 3（詳細はSupplementary Table）
- **次の段落への接続**: 集団内差異の地理的要因との関係を検証

### Figure 4a-e: 都道府県別 outgroup f3 地図
- **段落の役割**: 縄文人集団の地域的分化の有無を検証
- **主要な観察結果**:
  - 全縄文人サンプルで共通する地理的パターン（近畿地方で最低値、九州・東北で高値）
  - 居家以（Iyai、4個体プール）のf3値範囲：0.0955-0.0985（全体的に低い）
  - 他の縄文人のf3値範囲：0.106-0.110（サンプル間でほぼ同一）
- **重要な詳細**:
  - 5枚の地図：各遺跡（Iyai, Todoroki, Chidorigakubo, Mitsusawa, Funadomari）
  - 都道府県データ：11,069人から各県50個体をランダム抽出、8,464,930 SNPs
  - 詳細な統計値はSupplementary Table
- **次の段落への接続**: Iyaiが他の高カバレッジ縄文人とどのくらい離れているのか、直接的な比較を行う

---

## 3.3 現代日本人集団と縄文人サンプルの遺伝的近縁性の直接比較

### Figure 5: f4統計量解析
- **段落の役割**: 現代日本人がどの縄文人サンプルにより近縁かを直接検証
- **主要な観察結果**:
  - f4(Mbuti, Japanese, Iyai, Todoroki) = 0.000993 (Z = 3.001)
  - f4(Mbuti, Japanese, Iyai, Chidorigakubo) = 0.000982 (Z = 3.199)
  - f4(Mbuti, Japanese, Iyai, Mitsusawa) = 0.000904 (Z = 2.676)
  - f4(Mbuti, Japanese, Iyai, Funadomari) = 0.000617 (Z = 1.861)
  - 居家以を含まない組み合わせでは全て|Z| < 1
- **重要な詳細**:
  - 有意な差（|Z| > 3）を示したのはTodoroki及びChidorigakuboとの比較のみ
  - 現代日本人は早期集団と比べて、前期・中期の縄文人により近縁
  - 他の現代東アジア人（Korean, Han等）では全て非有意（Supplementary tableへ）
- **次の段落への接続**: 混合比率の定量化へ

### Figure 6: f4-ratio解析
- **段落の役割**: 現代日本人における縄文人系統の寄与率を定量化
- **主要な観察結果**:
  - Iyai使用時：縄文人成分 15.8% (SE = 0.0105, Z = 80.2)（対Han）、11.5% (SE = 0.0244, Z = 36.3)（対Korean）
  - 他の縄文人使用時：21.8-25.4%（対Han）、17.2-19.4%（対Korean）
  - 一貫してIyaiを用いたとき現代日本人集団における縄文人成分が低く算出される
- **重要な詳細**:
  - モデル a: Dai, b: Korean, x: Japanese, c: Jomon(Iyai, Todoroki, ), o: Mbuti
  - 使用SNP数：418449-601334（サンプルによって異なる）
  - 1-alphaが縄文人成分
- **次の段落への接続**: 系統関係の総括へ

---

## 3.4 系統関係と表現型の進化

### Figure 7: TreeMix解析
- **段落の役割**: 縄文人集団の分岐順序と時代との整合性を検証
- **主要な観察結果**:
  - Iyai（居家以、早期）が縄文人クレード内で最初に分岐（drift parameter ~0.14）
  - Todoroki（前期）、Chidorigakubo・Mitsusawa（中期）、Funadomari（後期）が後に分岐
  - 移住エッジ: ?
- **重要な詳細**:
  - ブートストラップ値: ?
  - 残差の評価: ?
  - 使用したSNP数とブロックサイズ: ?
- **次の段落への接続**: 系統関係から表現型へ

### Figure 8: ポリジェニックリスクスコア（PRS）
- **段落の役割**: 縄文人集団の表現型特性を現代日本人との違いに基づいて評価
- **主要な観察結果**:
  - 身長（Height）：両縄文人集団で負の値（低身長傾向）, BMIについても遺伝的に高い傾向。
  - 脂質代謝（TC, TG, LDL-C高、HDL-C低）→ エネルギー貯蔵能力の向上。糖代謝（BS, HbA1c高）→ 血糖維持能力、飢餓耐性。これらは「倹約遺伝子仮説」を支持
  - 免疫関連形質（Baso, CRP, Eosino）：好中球とWBC総数は高スコアとなり、細菌感染に対する即座の炎症反応能力が高いことを示唆している。一方好酸球、好塩基球は低スコアで、農耕生活によってもたらされる寄生虫感染リスクが縄文時代にはさほど高くなかったことを示唆。
  - 腎機能（eGFR高スコア）→ 腎機能良好、電解質バランス → 高タンパク食（狩猟）への適応を示唆
  - Iyaiと他の縄文人集団間でのPRSの高低を比較すると、腎機能（OtherJomonが高い）と心血管系（Iyaiが高い）で差異が見られた。Iyaiが内陸山間部の集団であり他が沿岸部であることから、塩分摂取量が低かったことを反映している可能性がある（詳しくはDiscussionで記述する予定）。

- **重要な詳細**:
  - 使用GWAS：Biobank Japan（BBJ）のJenger database（http://jenger.riken.jp/result）
  - P値閾値：0.01, 0.001, 0.0001の3段階（図はP < 0.01）
  - PRS計算：居家以4個体と他の縄文人4個体の2集団でアリル頻度を計算し、BETA値との積和
  - 現代日本人のPRSとの差分を表示
  - 謝辞：BBJとデータ元論文の引用が必要
  - 集団間比較：Log2 Fold Change (OtherJomon/Iyai)で表示

---

## 全体の流れのチェックリスト

- [ ] 集団構造（PCA/ADMIXTURE）→ 集団間関係（f3/f4）→ 混合比率 → 系統関係 → 表現型という論理的流れ
- [ ] 居家以（縄文早期）の特異性が一貫して示されている
- [ ] 各解析手法の相補性が明確
- [ ] 定量的データ（数値、統計量）が適切に記載されている
- [ ] 先行研究との整合性・新規性が明確

---

## 執筆時の注意事項

1. **サンプル表記**: 
   - 既報個体: F23 (Late Jomon, Hokkaido), I1 (Initial Jomon, Gunma)
   - 新規個体: T5 (Early Jomon, Kumamoto), I4/I15/I18 (Initial Jomon, Gunma), M3 (Middle Jomon, 4450 cal BP, Kanagawa), C3 (Middle Jomon, 5048 cal BP, Kanagawa)
   - 居家以遺跡：I1, I4, I15, I18の4個体（全て縄文早期）
   - カバレッジ: [後日記載 - 共同研究先への問い合わせが必要]
   - 年代測定: M3 (4450 cal BP), C3 (5048 cal BP), その他は[後日記載]

2. **専門用語**: 
   - f統計量は "f3 statistics", "f4 statistics" と表記
   - 時代区分: Initial Jomon (早期), Early Jomon (前期), Middle Jomon (中期), Late Jomon (後期)

3. **数値の表記**: 
   - f統計量: 小数点以下4桁（例: f3 = 0.2145）
   - 標準誤差: ± SE または (SE) 形式
   - P値: P < 0.05, P < 0.01, P < 0.001 の3段階

4. **図表の参照**: 
   - 初出: "Principal component analysis revealed..." (Figure 1)
   - 2回目以降: "As shown in Figure 1..." 

5. **統計的表現**:
   - 有意: "statistically significant (|Z| > 3)"
   - 非有意: "not significantly different from zero (|Z| < 3)"

6. **データセット情報**:
   - 1240K Allen Ancient DNA Resource
   - 330 East Asian individuals
   - 973,002 SNPs

7. **Results セクション執筆の基本原則**:

   **a) 冒頭での各解析の目的提示**
   - 各サブセクションの最初に、その解析で何を明らかにしようとしているかを1文で述べる
   - 例: "To assess the genetic relationships between Doigahama Yayoi individual, D1604, and other East Eurasian populations..."
   
   **b) 結果の客観的記述**
   - 数値データを中心に、観察された事実を淡々と記述
   - 解釈は最小限に留め、「suggesting」「indicating」程度の控えめな表現を使用
   - 詳細な解釈や意義付けはDiscussionに委ねる
   
   **c) 図表への言及方法**
   - 各図表を初めて言及する際は、その図が何を示しているかを簡潔に説明
   - 例: "The PCA plots, including the Doigahama Yayoi individual along with ancient and modern East Asians, are shown in Fig. 2."
   - 具体的な観察結果を図の括弧内で示す
   - 例: "positioned between the Jomon and continental East Asian clusters (Fig. 2A)"
   
   **d) 定量的情報の記載**
   - パーセンテージ、比率、統計値は必ず具体的な数値で示す
   - 例: "exhibited approximately 7% Jomon-related, 67% East Asian-related, and 26% Northeastern Siberian-related ancestries"
   - 範囲を示す場合は「approximately」「ranging from X to Y」を使用
   
   **e) 他研究との比較**
   - 先行研究との一致・不一致は事実として簡潔に述べる
   - 例: "consistent with previous studies [reference]"
   - 詳細な議論はDiscussionで展開
   
   **f) サブセクション間の接続**
   - 各サブセクションは独立して理解できるように書く
   - 前の解析結果を受けて次の解析を行う場合は、その関連性を明示
   
   **g) 技術的詳細の扱い**
   - 使用したプログラムやパラメータの詳細はMethods（またはSupplementary）へ
   - Resultsでは使用した手法名と主要なパラメータのみ簡潔に記載
   - 例: "using the qpF4ratio v400 program"
   
   **h) 統計的有意性の表現**
   - Z値、P値は具体的に記載
   - 有意性の判定基準は初出時に明記（例: "|Z| > 3"）
   - エラーバーの説明も明確に（例: "error bars representing the range of |Z| ≤ 1"）
   
   **i) ネガティブな結果の報告**
   - 有意でない結果や期待と異なる結果も客観的に報告
   - 例: "did not yield any positive results supporting..."
   
   **j) 図表のキャプション的説明の回避**
   - 図表の詳細な説明は図表のキャプションに任せる
   - 本文では主要な発見のみを記述

8. **避けるべき表現**:
   - 過度に解釈的な表現（"clearly demonstrates", "proves"など）
   - 冗長な説明や繰り返し
   - Methods的な詳細（サンプル調製法、詳細なパラメータ設定など）
   - Introduction的な背景説明
   - Discussion的な深い考察や推測

9. **文体の統一**:
   - 過去形を基本とする（実験結果の記述）
   - 能動態を優先的に使用
   - 一文は簡潔に（複雑な内容は複数の文に分割）
   - 接続詞を効果的に使用して論理的な流れを作る
   - 説明的・冗長な印象を与えることを避ける
   - 繰り返し表現ややや過剰な強調表現（例："clearly separated", "strongly supports", "complete absence"）を適度に抑えると、学術的な中立性が高まる。
   - 視覚データの言及（Figure 1, 2a-d）に対する言葉の補足も改善の余地あり。現状でも正確だが、アクセプト率を高めるには、図の生物学的解釈に一言加えるとよい。