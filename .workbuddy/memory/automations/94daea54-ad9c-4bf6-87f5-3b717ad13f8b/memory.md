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
