# 密封件.cn

O 型圈规格查询与选型工具站，纯静态，零后端。

- **站点域名**：密封件.cn（`xn--5nq252acf.cn`）
- **上线地址**：https://xn--5nq252acf.cn
- **数据来源**：GB/T 3452.1-2005 G 系列，完整展开 305 条规格组合

## 仓库分支说明

| 分支 | 内容 | 说明 |
|---|---|---|
| `main` | 站点源码 | `build.py` + `content/` + `templates/` + `data/`，改内容改这里 |
| `gh-pages` | 构建产物 | `public/` 的内容，GitHub Pages 从这里发布，**不要手动改** |

## 本地构建

```bash
pip install markdown idna
python build.py      # 产出 public/
```

改完内容后重新构建，把 `public/` 的内容同步到 `gh-pages` 分支即可更新线上。

## 询单接收端配置

询单表单提交后直接推送到飞书群机器人（浏览器直连，飞书 webhook 已开放 CORS，无需后端）。

配置写在 `config.local.json`（**已在 .gitignore 中排除，不会进仓库**）：

```json
{
  "feishu_webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/xxxx",
  "feishu_keyword": "询单",
  "form_endpoint": ""
}
```

也可以双击 `配置询单接收端.bat` 交互式配置，脚本会真发一条测试卡片到群里验证通道。

> 安全提示：webhook 地址必然出现在前端源码里（纯静态站的固有限制）。
> 务必在飞书群机器人的「安全设置」中启用**自定义关键词**（关键词填 `询单`），
> 否则任何人拿到地址都能往群里灌消息。不要用「签名校验」——密钥放前端等于公开。

## 目录结构

```
build.py                 构建脚本（读取 content/data/templates，产出 public/）
gen_data.py              规格与材质数据生成（305 条规格 / 10 种材质 / 20 类介质）
setup_form.py            询单接收端交互式配置
templates/               layout.html / tool.html / contact.html
content/                 8 篇技术文章（含不写进仓库的草稿）
data/                    规格、材质、介质、选型规则四份 JSON
static/                  style.css
tests/                   本地模拟飞书端点 + 表单回归测试
worker/                  Cloudflare Worker 中转版（可选，用于隐藏 webhook 地址）
```
