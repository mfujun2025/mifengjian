# 自动化执行记录 · 密封件.cn 每日发文

> 本文件只记高层执行摘要，不存正文内容。
> 注：项目历史日志落在 `C:\Users\Huawei\.workbuddy\2026-09-14-21-07-05\.workbuddy\memory\YYYY-MM-DD.md`（上一级目录），本文件为自动化专用索引。

## 2026-09-16 · 第 3 篇

| 项 | 值 |
|---|---|
| 选题 | `pu-o-ring-guide`（选题池第一条未勾选） |
| 标题 | 聚氨酯 PU：耐磨抗挤出最强，但它的水解短板会咬人 |
| 分类 | materials / 材质百科，order 11 |
| 篇幅 | 正文 2689 中文字，7 节 + 1 个三级标题，6 个表格 |
| 构建 | `build.py` 成功 → 19 个 HTML（较上次 +1）、sitemap 18 条 |
| 发布 | `deploy.py --source` 成功 → gh-pages `db6981bd`（28 文件）、main `d53a0c58`（34 文件） |
| 验收 | 新文章 URL **HTTP 200（首次即通）**；线上 6 个 table、含 `/tool/` 与 `/contact/`；sitemap 含该 URL；`/materials/` 列表页与首页卡片均已收录 |
| 结果 | ✅ 全链路成功，无失败项 |

**本次新增的经验（重要）**

- ⚠️ **长中文 markdown 用 `Write` 覆盖时出现过两次「正文整体重复」**：文件 front matter 之后被完整追加了第二遍正文（首次 6450 字、二次 5310 字）。
- **快速自检法**：写完立刻统计「中文字数 / `^## ` 数 / `^\|---` 表格数 / 标志字符串出现次数」。任一数量翻倍即为重复，比读全文快得多。
- **去重法**：用 Python 按 offset 截断到第一遍正文末尾（第一个 `\n---\n` 结束处），再补回结尾段。**不要用 Edit 去重**——重复内容会导致 `old_string` 不唯一而报错。
- **规避策略**：长文一次性 `Write` 完整版（单次写入更可靠）；需要大改时重新整体 `Write` 覆盖，避免多次 Edit 叠加追加。
- 素材核实：写 PU 前查了 `data/materials.json` 的 `temp_min`/`temp_max`/`peak`/`good`/`bad` 全套字段，文章口径与 `/tool/` 推荐一致（PU 在 air/ozone/glycol/hydraulic_mineral/engine_oil 为推荐，water_cold→水解、steam/酮/酯/酸碱/醇/芳香烃/刹车油/磷酸酯为禁区）。
- 联网核实了水解机理（酯键自催化水解、70℃ 水中约 200h vs 醚型 >1000h）、耐磨倍数（NBR 的 3~5 倍）、耐压（静态 ≤40MPa / 带挡圈 60MPa+）、储存（SAE AS5316 中 AU/EU 保鲜 5 年、湿度 <65%）。
- 选题池已推进到材质百科第 4 条，剩下 PTFE / FVMQ / FFKM / CR 四条。
