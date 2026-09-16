# 自动化执行记录 · 密封件.cn 每日发文

> 本文件只记高层执行摘要，不存正文内容。
> 注：项目历史日志落在 `C:\Users\Huawei\.workbuddy\2026-09-14-21-07-05\.workbuddy\memory\YYYY-MM-DD.md`（上一级目录），本文件为自动化专用索引。

## 2026-09-15 · 第 2 篇

| 项 | 值 |
|---|---|
| 选题 | `hnbr-o-ring-guide`（选题池第一条未勾选） |
| 标题 | 氢化丁腈 HNBR：NBR 加氢之后，为什么多扛 50℃、还耐臭氧 |
| 分类 | materials / 材质百科，order 10 |
| 篇幅 | 正文 2272 中文字，7 节，4 个表格 |
| 构建 | `build.py` 成功 → 18 个 HTML（较上次 +1）、sitemap 17 条 |
| 发布 | `deploy.py --source` 成功 → gh-pages `b1c521f7`（27 文件）、main `6ecd6063`（32 文件） |
| 验收 | 新文章 URL **HTTP 200（首次即通）**；sitemap 含该 URL；`/materials/` 列表页与首页卡片均已收录 |
| 结果 | ✅ 全链路成功，无失败项 |

**本次新增的经验**
- 选题池已推进到材质百科第 2 条（剩下 PU / PTFE / FVMQ / FFKM / CR 五条）。
- `build.py` 输出的是产物文件清单，没有「构建完成」之类的汇总行；判断成功看「无报错 + HTML 计数 +1」。
- 材质类文章落笔前必须 `Read data\materials.json` 核对该材质的 `temp_min`/`temp_max`/`peak`/`good`/`bad`，文章口径要和 `/tool/` 推荐结果一致（本次 HNBR：-40~150℃、峰值 165℃）。
- 已把「数据一致性」和「构建产物校验命令」两节补进 skill `seal-cn-content-update`。
