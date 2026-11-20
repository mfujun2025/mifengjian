# 密封件.cn 每日发文自动化 — 执行摘要

## 2026-11-11 执行记录

- **选题**：选题池已全部勾完，按文末「拓展方向」新挖 → `valve-seal-repair`（拓展方向 2·维修实例，阀门为工业高频设备且全站尚无单篇；与 water-treatment-o-ring 仅材料层面提及泵阀不重叠）。
- **文章**：`content/valve-seal-repair.md`，order=67，category=articles。正文约 2100 字，含 4 个 Markdown 表格（三类漏点对照、阀杆填料选型、阀座软密封材质、法兰垫片选型），结尾引导 /tool/ 与 /contact/。
- **数据一致性**：阀座材质耐温与介质红线（NBR/EPDM/FKM/PTFE）严格对齐 `data/materials.json`，无矛盾。
- **关键事实来源**：联网核实阀门三类漏点、柔性石墨填料、阀座弹性体介质红线、法兰垫片与螺栓力矩、GB/T 13927 压力试验（百度百科 + Fluid Sealing Association 手册）。
- **构建**：`build.py` 成功，新页面 `public/articles/valve-seal-repair/index.html`；全站 75 个 HTML、sitemap 74 条；抽查表格数=4、/tool/ 与 /contact/ 链接均在。
- **发布**：`deploy.py --source` 成功；gh-pages 上传 84 文件、main 同步 113 文件。
- **验收**：线上 `https://xn--5nq252acf.cn/articles/valve-seal-repair/` 返回 200；sitemap 与 /articles/ 列表页均收录。一次通过，无需轮询。

## 2026-11-12 执行记录

- **选题**：`valve-seal-repair` checkbox 漏更新（11-11 已发布），先补勾；取扩展方向新挖 → `pump-mechanical-seal-guide`（泵用机械密封，全站无专文；o-ring-vs-oil-seal 仅类型对比、water-treatment 仅材质层面提及泵，不重叠）。
- **文章**：`content/pump-mechanical-seal-guide.md`，order=68，category=articles。正文约 2200 字，4 个 Markdown 表格（填料 vs 机封对比、摩擦副配对、API 682 冲洗方案、泄漏原因倒推），结尾引导 /tool/ 与 /contact/。
- **数据一致性**：辅助密封圈红线（NBR/FKM/EPDM/FFKM/PTFE）严格对齐 `data/materials.json`；碱液禁用 FKM、蒸汽热水用 EPDM、酮酯溶剂用 FFKM/PTFE。
- **关键事实来源**：联网核实 GB/T 33509-2017 摩擦副选配原则、API 682 Plan 11/13/21/23/31/32/52/53、机封泄漏判据（几乎不漏/几滴内，成线即异常）、SiC 耐温约 800℃、Plan 32 冲洗压力高出密封腔 0.1~0.15MPa（邦瀑泵业、上海水泵集团、流程工业、MidstreamCalculator、邦威泵业）。
- **构建**：`build.py` 成功，新页面 `public/articles/pump-mechanical-seal-guide/index.html`；全站 85 个文件、68 篇文章；抽查表格=4、/tool/ 链接=4 处、sitemap 与 /articles/ 列表页均收录。
- **发布**：`deploy.py --source` 成功；gh-pages 85 文件、main 同步 114 文件。
- **验收**：线上文章页首次请求即返回 200；sitemap 含新 URL、/articles/ 列表页 200 且收录。一次通过。

## 2026-11-13 执行记录

- **选题**：选题池已全部勾完，按拓展方向 2（维修实例）新挖 → `gearbox-seal-leak-repair`（减速机漏油维修，减速机为高频设备且全站无专文；与 valve/pump/机床/叉车/空压机各实例篇不重叠）。
- **文章**：`content/gearbox-seal-leak-repair.md`，order=69，category=articles。正文约 2200 字，2 个 Markdown 表格（四类漏点定位、油封材质 NBR/HNBR/FKM 选材），结尾引导 /tool/ 与 /contact/。
- **数据一致性**：油封材质红线（NBR 不耐臭氧/热水蒸汽、HNBR 不耐热水蒸汽、FKM 不耐酮酯与热水蒸汽）严格对齐 `data/materials.json`。
- **关键事实来源**：联网核实（强星减速机、威高传动、川奥星、泰隆减速机、辉泰科技、兴鸿凯）：通气帽内压机理、四类漏点分类、油温红线（正常 ≤80℃、紧急停机 85℃、矿物油轴封 ≤90℃/合成油 100℃）、轴封温差异常判据（高出箱体 20℃）、油位 1/2~2/3、换油周期（新机 300~500h 首换，之后 3000~6000h 或 6~12 个月）、轴承晃动测试、唇口方向与导向套安装。
- **构建**：build.py 成功，86 个文件、69 篇文章；抽查表格=2、/tool/ 链接=3、/contact/ 链接=3，sitemap 与 /articles/ 列表页均收录。
- **发布**：deploy.py --source 成功；gh-pages 86 文件（commit 5a3a0e4f）、main 116 文件（commit f7bcdb21）。
- **验收**：线上文章页首次请求即 200；sitemap 含新 URL、/articles/ 列表页 200 且收录。一次通过。
- **选题池**：已追加条目并标记「已发布 2026-11-13」。

## 2026-11-14 执行记录

- **选题**：选题池全部勾完，按拓展方向 3（参数深挖）新挖 → `high-temperature-seal-guide`（高温 200℃+ 密封，与深冷篇 cryogenic-lng-seal-guide 形成对称，各单一材质篇仅讲自身边界、无横向温域决策文）。
- **文章**：`content/high-temperature-seal-guide.md`，order=70，category=articles。正文约 2070 汉字，3 个 Markdown 表格（橡胶高温排名与禁区、石墨与金属接棒方案、按温度带决策表），结尾引导 /tool/ 与 /contact/，文末附参考来源。
- **数据一致性**：橡胶耐温口径严格对齐 `data/materials.json`（VMQ/FKM 200/230、EPDM 150/180、HNBR 150/165、NBR 100/120、FFKM 300/320、PTFE 包覆 260）；介质红线（FKM 不耐蒸汽酮酯、EPDM 不耐油、VMQ 不耐油与蒸汽）均与工具页一致。
- **关键事实来源**：联网核实——柔性石墨氧化气氛长期 ≤450℃/短期 550℃、增强型非氧化约 1600℃（百度百科石墨垫片+恒途科技）；金属缠绕垫 -196~650℃、氧化介质按填充料打折、紫铜垫连续约 260℃（百度百科+化工仪器网）；Arrhenius 每升 10℃ 老化速率翻倍为经验法则并注明 ISO 11346 适用边界警告。
- **构建**：build.py 成功，87 个文件、70 篇文章；抽查表格=3、/tool/ 与 /contact/ 链接均在、sitemap 与 /articles/ 列表页均收录新 URL。
- **发布**：deploy.py --source 成功；gh-pages 87 文件（dd0ea575）、main 118 文件（ddf6bfe2）。
- **验收**：线上文章页首次请求即 200；sitemap 含新 URL、/articles/ 列表页 200 且收录。一次通过。
- **选题池**：已追加条目并标记「已发布 2026-11-14」。

## 2026-11-17 执行记录

- **选题**：选题池全勾完，去重后新挖 → `hydraulic-fitting-seal-guide`（液压管接头密封结构，全站此前仅在泄漏排查/类型对比篇一句话带过）。去重时否掉三个候选：表面粗糙度（沟槽标准篇专节已覆盖）、装配润滑（安装损伤篇专表已覆盖）、换油兼容性（液压系统篇开篇案例+表格已覆盖）。
- **文章**：`content/hydraulic-fitting-seal-guide.md`，order=73，category=articles。正文 1996 汉字，7 个 H2（含结论与参考来源），2 个表格（五类接头形式对照、五步漏点排查），文末按 MLA 列 5 条参考来源。
- **关键事实来源**：联网核实 ISO 8434 家族（24° 卡套 ISO 8434-1/DIN 2353、JIC 37° ISO 8434-2/SAE J514、ORFS ISO 8434-3/SAE J1453、60° 锥 ISO 8434-6、SAE 法兰 ISO 6162）、LL/L/S 系列压力量级、ORFS 约 420 bar、DKO 锥面 O 圈变体、卡套预装与插底要求、力矩增加后 1/4~1/2 圈、禁涂密封胶（冲入系统堵阻尼孔）、BSPP/BSPT/NPT 制式差异（PTS Group、RR Hydraulics、倍润液压、昊可流体、帕克橡塑、利旺流体）。来源无发布日期的一律写「访问于 2026-11-17」，不编年份。
- **数据一致性**：O 圈材质红线对齐 `data/materials.json`（矿物油 NBR -30~100℃、FKM 不耐酮酯/热水蒸汽、磷酸酯须 EPDM、EPDM 不耐矿物油）。卡套重复使用「允许与否」来源冲突，按厂家说明+检查磨损处理，不写绝对结论；力矩数值来源单位可疑，改为「按厂家力矩或圈数」不写具体数字。
- **构建**：build.py 成功，90 个文件、73 篇文章；抽查表格=2、/tool/=3、/contact/=3、sitemap 与列表页均收录。
- **发布**：deploy.py --source 成功；gh-pages 90 文件（7facc1b8）、main 123 文件（6c10f24c）。
- **验收**：首次文章页/列表页返回 000（连接未就绪，sitemap 已含新 URL），等待 35 秒后轮询第 2 次文章页 200、列表页 200。未重复推送。
- **待办备注**：后续候选——液压缸整套密封包配置、矿山/造纸/船舶等设备维修实例、标准互换换算（须防与 metric-vs-inch/jis/as568 重叠）。

## 待办 / 备注
- 后续若选题池再次全勾，可继续从拓展方向挖（维修实例已完成：空压机/注塑机/叉车/机床/阀门/泵/减速机；参数深挖已完成：深冷/超高压/线速度/高温；采购实务已完成：报价单/审厂/渠道层级；下一候选：液压缸维修实例、替代换算类决策树补充、饮用水之外行业合规补充）。

## 2026-11-15 执行记录

- **选题**：选题池全部勾完，按拓展方向 4（采购实务）新挖 → `seal-purchase-channel-guide`（密封件采购渠道层级对比，方向 4 尚未覆盖项；与 seal-quotation-guide（报价单）、seal-supplier-audit-guide（审厂）、o-ring-purchase-spec（规格书）、import-o-ring-substitution（国产替代）不重叠）。
- **文章**：`content/seal-purchase-channel-guide.md`，order=71，category=articles。正文约 2100 汉字，2 个 Markdown 表格（四渠道横向对比、按采购场景选渠道决策表），结尾引导 /tool/ 与 /contact/。
- **关键事实来源**：联网核实（Eurobearing、贝拓尔液压/义乌网、NOK 代理头条文）——NBR 冒充 FKM 为高频造假手法、同型号 NBR/FKM 价差 3~5 倍、真 FKM 鉴别法（130℃ 矿物油浸泡 72h 尺寸硬度不变，NBR 溶胀变软）、燃烧法/比重法初判（FKM 比重约 1.8~2.0、NBR 约 1.2~1.3）、合同标注材质代号与耐温范围。
- **数据一致性**：材质红线（NBR 连续上限约 100℃、硅橡胶/EPDM 不耐矿物油、FKM 不耐酮酯与热水蒸汽、PTFE 无弹性）均与 `data/materials.json` 口径一致。
- **构建**：build.py 成功，88 个文件、71 篇文章；抽查表格=2、/tool/ 链接=4 处、sitemap 与 /articles/ 列表页均收录新 URL。
- **发布**：deploy.py --source 成功；gh-pages 88 文件（55f1e0b7）、main 120 文件（d54ddd01）。
- **验收**：线上文章页首次请求即 200；sitemap 含新 URL、/articles/ 列表页 200 且收录。一次通过。
- **选题池**：已追加条目并标记「已发布 2026-11-15」。

## 2026-11-16 执行记录

- **选题**：选题池全部勾完，新挖 → `steam-hot-water-seal-guide`（蒸汽/热水介质工况，全站无专文；epdm-o-ring-guide 仅讲材质本身、high-temperature-seal-guide 仅讲温度维度、water-treatment-o-ring 讲耐氯，不重叠）。已追加到选题池第十章并标记「已发布 2026-11-16」。
- **文章**：`content/steam-hot-water-seal-guide.md`，order=72，category=articles。正文 1920 汉字，6 个 H2，2 个 Markdown 表格（表压-饱和温度对照、橡胶蒸汽排名对照），结尾引导 /tool/ 与 /contact/。
- **关键事实来源**：联网核实——表压/饱和温度对照（0.2→133.5℃ … 1.6→203.4℃，IAPWS-IF97，多源一致）、0.5MPa 绝压 151.9℃ vs 表压 158.8℃、蒸汽四类失效机理（水解/配合剂抽出/压缩永久变形激增/爆炸性减压 RGD）、硫磺硫化 EPDM 蒸汽 ~120℃ vs 过氧化物硫化 130~150℃、标准 FKM 蒸汽中 ≤120℃、FKM 特种牌号（ETP/GF）与 FFKM 逐牌号确认（Kalrez 6375 推荐 vs 4079 不推荐）、FEPM/AFLAS 为油+蒸汽折中、柔性石墨 450℃/金属缠绕垫 -196~650℃（与高温篇口径一致）。
- **数据一致性**：橡胶蒸汽排名严格对齐 `data/materials.json`（EPDM good 蒸汽、FKM/NBR/VMQ/PU/HNBR/FVMQ/CR bad 蒸汽、FFKM/PTFE 包覆 good）；HNBR 有一来源称水/蒸汽 150℃，按站内口径写为「不耐长期高温水/蒸汽水解」不采用。
- **构建**：build.py 成功，89 个文件（+1）、72 篇文章；抽查表格=2、/tool/ 链接=3、/contact/ 链接=3、sitemap 与 /articles/ 列表页均收录。
- **发布**：deploy.py --source 成功；gh-pages 89 文件（8c95b49d）、main 122 文件（3d7e7373）。
- **验收**：线上文章页首次请求即 200；sitemap 含新 URL、/articles/ 列表页 200 且收录。一次通过。
- **待办备注**：拓展方向候选余量——液压缸维修实例、饮用水外行业合规补充、标准互换换算类（需先防与 metric-vs-inch/jis/as568 重叠）。

## 2026-11-18 执行记录

- **选题**：选题池全勾完。去重时否掉「液压缸整套密封包配置」（与 excavator-seal-guide 六部位配置表实质重叠）；按拓展方向 3·密封结构深挖新挖 → `x-ring-seal-guide`（星形圈/X 型圈，全站仅 reciprocating-seal-types 一句话带过、无专文；与往复选型篇、三类密封件对比篇、PU 材质篇均不重叠）。已追加选题池第十节并标记已发布。
- **文章**：`content/x-ring-seal-guide.md`，order=74，category=articles。正文 2363 汉字，6 个主章节 H2（+结论+参考来源），4 个表格（O/X 对照、"沟槽通用"核对清单、材质红线、换不换决策），结尾引导 /tool/ 与 /contact/，文末按 MLA 列 6 条来源。
- **关键事实来源与口径处理**：联网核实——Trelleborg Quad-Ring 双作用四唇定义（每侧两条密封线、唇间储油、分型飞边藏在唇间凹谷）、Parker ORD 5700 螺旋失效七因素与启动/运转摩擦两状态、ISO 3601-1/-2 只管 O 型圈尺寸与密封座不替星形圈互换背书。**重要口径分歧**：国内厂商宣传「AS568 同尺寸沟槽完全通用」，Trelleborg/ISO 要求按所选产品沟槽图、名义尺寸相同≠可互换（能装入≠验收合格）；文章按「有前提」处理，不写绝对结论。压力数字各来源冲突（30~50MPa 不等），按用户「宁可少写不写错」不给定值，仅写「与 O 圈同量级、由间隙/硬度/挡圈决定」；摩擦降 10~30%、单价 3~6 倍、压缩量等均标「厂商口径」。
- **数据一致性**：材质红线严格对齐 `data/materials.json`（NBR -30~100、HNBR -40~150、FKM -20~200、FFKM -20~300、PU -30~80、VMQ -60~200）；硅橡胶/EPDM 不耐矿物油、FKM 不耐酮酯热水蒸汽、PU 水解短板均与工具页一致。
- **构建**：build.py 成功；HTML 81→82（+1）、sitemap 80→81；内容文章 74 篇、工具页注入 305 条规格。抽查新页表格=4、/tool/=4、/contact/=4，sitemap 与 /articles/ 列表页均收录。
- **发布**：deploy.py --source 成功；gh-pages 91 文件（f4b8ec37）、main 125 文件（3f6c2167）。
- **验收**：线上文章页首次请求即 200；线上 sitemap 与 /articles/ 列表页均含新 URL。一次通过，无需轮询重试。
- **待办备注**：后续候选——液压缸整套维修实例、矿山/造纸/船舶设备维修实例、标准互换换算类（须防与已有标准篇重叠）。
