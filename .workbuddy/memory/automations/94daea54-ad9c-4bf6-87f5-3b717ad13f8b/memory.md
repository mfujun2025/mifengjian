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

## 待办 / 备注
- 选题池末尾已追加新选题条目并标记「已发布 2026-11-12」。
- 后续若选题池再次全勾，可继续从拓展方向挖（泵机封已做，下一候选：减速机/液压缸维修实例，或密封渠道层级对比）。
