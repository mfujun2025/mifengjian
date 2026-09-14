# -*- coding: utf-8 -*-
"""
密封件.cn 静态站点构建脚本。

  python build.py

读取：content/*.md（带 front matter）、data/*.json、templates/layout.html、static/
产出：public/  —— 可直接部署到 GitHub Pages 的完整站点
"""
import json
import os
import re
import shutil
import datetime

import markdown

BASE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(BASE, "content")
DATA = os.path.join(BASE, "data")
TPL = os.path.join(BASE, "templates")
STATIC = os.path.join(BASE, "static")
PUB = os.path.join(BASE, "public")
PUB_DATA = os.path.join(PUB, "data")

DOMAIN_ASCII = "xn--5nq252acf.cn"          # 密封件.cn
DOMAIN_CN = "密封件.cn"
SITE_URL = "https://" + DOMAIN_ASCII
YEAR = "2026"
BUILD_TIME = datetime.datetime.now().strftime("%Y-%m-%d")

NAV_ITEMS = [
    ("/", "首页"),
    ("/tool/", "规格查询"),
    ("/materials/", "材质百科"),
    ("/articles/", "技术文章"),
    ("/faq/", "常见问题"),
    ("/contact/", "选型咨询"),
]

# ---------------------------------------------------------------- 询单接收配置
# 两种接法，二选一。两者都留空时表单进入「演示模式」：前端校验照跑，
# 但不向任何第三方发送数据，而是提示访客复制内容另行发送。

# 【接法 A · 最省事】飞书群机器人 Webhook，浏览器直连（飞书 webhook 已开放 CORS）
#   飞书群 → 右上角 ··· → 设置 → 群机器人 → 添加机器人 → 自定义机器人
#   安全设置选「自定义关键词」，关键词填：询单
#   把生成的 https://open.feishu.cn/open-apis/bot/v2/hook/xxx 填进 config.local.json

# 【接法 B · 更稳】Cloudflare Worker 中转，源码见 worker/feishu-form-proxy.js
#   webhook 不暴露在前端，另带来源校验、限流、字段裁剪
#   部署好后把 Worker 地址（https://xxx.yyy.workers.dev）填进 config.local.json

# 配置读取优先级：config.local.json  >  环境变量（GitHub Secrets / 命令行）
#   config.local.json 内容示例：
#     { "feishu_webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/xxxx",
#       "feishu_keyword": "询单",
#       "form_endpoint": "" }
#   不填也可以：此时表单进入「演示模式」，前端校验照跑但不向任何第三方发送数据。
CONFIG_LOCAL = os.path.join(BASE, "config.local.json")
LOCAL_CFG = {}
if os.path.isfile(CONFIG_LOCAL):
    try:
        with open(CONFIG_LOCAL, "r", encoding="utf-8") as f:
            LOCAL_CFG = json.load(f) or {}
    except Exception as e:
        print("  [警告] config.local.json 读取失败，已忽略：%s" % e)


def cfg(key, env_name, default=""):
    v = LOCAL_CFG.get(key)
    if v is None or (isinstance(v, str) and not v.strip()):
        v = os.environ.get(env_name) or default
    return str(v or "").strip()


FEISHU_WEBHOOK = cfg("feishu_webhook", "SEAL_FEISHU_WEBHOOK")
FEISHU_KEYWORD = cfg("feishu_keyword", "SEAL_FEISHU_KEYWORD", "询单") or "询单"
FORM_ENDPOINT = cfg("form_endpoint", "SEAL_FORM_ENDPOINT")

MD = markdown.Markdown(extensions=["tables", "fenced_code", "attr_list", "sane_lists"])


# ------------------------------------------------------------------ 工具函数
def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write(rel, text):
    p = os.path.join(PUB, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    return p


def to_html(md_text):
    MD.reset()
    return MD.convert(md_text)


def render_layout(title, desc, keywords, canonical, body, ogtype="website", jsonld=""):
    tpl = read(os.path.join(TPL, "layout.html"))
    nav = "\n".join(
        '      <a href="%s"%s>%s</a>' % (href, ' class="on"' if canonical.startswith(href) and href != "/" else "", name)
        for href, name in NAV_ITEMS
    )
    out = (tpl
           .replace("{{TITLE}}", title)
           .replace("{{DESC}}", desc)
           .replace("{{KEYWORDS}}", keywords)
           .replace("{{CANONICAL}}", canonical)
           .replace("{{OGTYPE}}", ogtype)
           .replace("{{NAV}}", nav)
           .replace("{{BODY}}", body)
           .replace("{{JSONLD}}", jsonld)
           .replace("{{YEAR}}", YEAR))
    return out


def jsonld(obj):
    if not obj:
        return ""
    return '<script type="application/ld+json">\n%s\n</script>' % json.dumps(obj, ensure_ascii=False, indent=1)


# ------------------------------------------------------------------ 内容解析
def parse_content():
    items = []
    for fn in sorted(os.listdir(CONTENT)):
        if not fn.endswith(".md"):
            continue
        raw = read(os.path.join(CONTENT, fn))
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw, re.S)
        if not m:
            raise ValueError("缺少 front matter: " + fn)
        meta_raw, body_md = m.group(1), m.group(2)
        meta = {}
        for line in meta_raw.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        meta["order"] = int(meta.get("order", 99))
        meta["body_md"] = body_md.strip()
        meta["file"] = fn
        items.append(meta)
    items.sort(key=lambda x: x["order"])
    return items


# ------------------------------------------------------------------ 页面片段
def article_card(a):
    return (
        '<div class="aitem">\n'
        '  <h3><a href="/articles/%s/">%s</a></h3>\n'
        '  <p>%s</p>\n'
        '  <div class="meta"><span>%s</span><span>%s</span></div>\n'
        '</div>' % (a["slug"], a["title"], a["desc"], a.get("category_name", ""), a.get("date", ""))
    )


def build_home(articles):
    mats = [a for a in articles if a.get("category") == "materials"]
    arts = [a for a in articles if a.get("category") != "materials"]
    specs = json.loads(read(os.path.join(DATA, "o-ring-specs.json")))
    matdata = json.loads(read(os.path.join(DATA, "materials.json")))
    media = json.loads(read(os.path.join(DATA, "media.json")))["media"]

    body = """
<div class="hero">
  <div class="wrap">
    <h1>O 型圈规格查询与选型参考</h1>
    <p>按 GB/T 3452.1-2005（等同 ISO 3601-1）整理的国标 O 型圈规格库，配一套能直接用的选型工具：查尺寸、拿旧件实测值找最接近规格、按温度与介质自动推荐材质并排除不适用材质。</p>
    <div class="btns">
      <a class="btn" href="/tool/">打开规格查询工具</a>
      <a class="btn line" href="/materials/">看材质百科</a>
    </div>
    <div class="stats">
      <div><b>{n_specs}</b><span>条标准规格组合</span></div>
      <div><b>{n_mats}</b><span>种常用材质</span></div>
      <div><b>{n_med}</b><span>类介质兼容规则</span></div>
      <div><b>0</b><span>后端依赖，纯前端</span></div>
    </div>
  </div>
</div>

<section class="tight">
  <div class="wrap">
    <h2 class="sec">三个功能，覆盖选型的全部环节</h2>
    <p class="sub">工程师实际要做的三件事：核对图纸尺寸、拿实物找规格、按工况定材质。工具把这三件事都做完了。</p>
    <div class="cards">
      <div class="card">
        <div class="tagline">功能一</div>
        <h3>尺寸查询</h3>
        <p>输入内径、截面或外径任一项即可查，自动带出对应公差。外径按 d1 + 2×d2 计算，不用手算。</p>
        <ul><li>支持组合条件缩小范围</li><li>内径公差按标准分档自动匹配</li><li>无结果时给出邻近标准尺寸</li></ul>
        <a class="more" href="/tool/">立即查询 →</a>
      </div>
      <div class="card">
        <div class="tagline">功能二</div>
        <h3>近似匹配</h3>
        <p>旧圈拆下来实测内径与截面，输入实测值，按匹配度排序给出最接近的标准规格，不用翻手册。</p>
        <ul><li>匹配度百分比量化偏差</li><li>截面偏差权重更高，结果更符合实际</li><li>提示“偏差偏大、需确认安装空间”</li></ul>
        <a class="more" href="/tool/">试试匹配 →</a>
      </div>
      <div class="card">
        <div class="tagline">功能三</div>
        <h3>材质选型</h3>
        <p>输入长期工作温度与接触介质，先按耐温过滤，再用介质黑名单排除不兼容材质，并逐条给出排除原因。</p>
        <ul><li>10 种材质的耐温与耐介质矩阵</li><li>排除项写明具体原因，不是只给结论</li><li>附带硬度与压缩率建议</li></ul>
        <a class="more" href="/tool/">开始选型 →</a>
      </div>
    </div>
  </div>
</section>

<section class="tight" style="background:#fff;border-top:1px solid var(--line);border-bottom:1px solid var(--line)">
  <div class="wrap">
    <h2 class="sec">材质百科</h2>
    <p class="sub">三种最常用材质的深入拆解：它们各自的耐温边界、耐受介质、明确禁区，以及什么时候该换成别的材质。</p>
    <div class="cards">
      {mat_cards}
    </div>
    <p style="margin-top:20px"><a href="/materials/">查看全部材质内容 →</a></p>
  </div>
</section>

<section class="tight">
  <div class="wrap">
    <h2 class="sec">技术文章</h2>
    <p class="sub">规格怎么读、压缩率怎么取、标准能不能互换、失效了怎么反推原因。</p>
    <div class="alist">
      {art_cards}
    </div>
    <p style="margin-top:20px"><a href="/articles/">查看全部技术文章 →</a></p>
  </div>
</section>

<section class="tight">
  <div class="wrap">
    <h2 class="sec">规格数据说明</h2>
    <p class="sub">本站规格数据按 GB/T 3452.1-2005 G 系列（一般应用）整理，共 {n_specs} 条组合，覆盖 5 个标准截面：1.8 / 2.65 / 3.55 / 5.3 / 7.0 mm。</p>
    <div class="cards">
      <div class="card"><h3>数据来源</h3><p>GB/T 3452.1-2005《液压气动用O形橡胶密封圈 第1部分：尺寸系列及公差》，等同采用 ISO 3601-1。</p></div>
      <div class="card"><h3>计算规则</h3><p>外径 d3 = 内径 d1 + 2 × 截面 d2。公差为标称值，实际以标准原文与厂家实测报告为准。</p></div>
      <div class="card"><h3>使用边界</h3><p>数据用于设计选型、采购比对与旧件识别；正式定型前请做介质相容性与压缩永久变形验证。</p></div>
    </div>
  </div>
</section>
""".format(
        n_specs=specs["meta"]["count"],
        n_mats=matdata["meta"]["count"],
        n_med=len(media),
        mat_cards="\n      ".join(
            '<div class="card"><h3><a href="/articles/%s/">%s</a></h3><p>%s</p></div>' % (a["slug"], a["title"], a["desc"])
            for a in mats
        ),
        art_cards="\n      ".join(article_card(a) for a in arts),
    )

    ld = jsonld([
        {"@context": "https://schema.org", "@type": "WebSite", "name": DOMAIN_CN, "url": SITE_URL,
         "inLanguage": "zh-CN",
         "potentialAction": {"@type": "SearchAction", "target": SITE_URL + "/tool/?q={search_term_string}",
                             "query-input": "required name=search_term_string"}},
        {"@context": "https://schema.org", "@type": "Organization", "name": DOMAIN_CN, "url": SITE_URL,
         "description": "O 型圈规格查询与密封选型参考站"},
    ])
    return render_layout(
        "O型圈规格查询工具 | %s 尺寸表·材质选型·GB/T 3452.1 标准规格" % DOMAIN_CN,
        "国标 O 型圈规格查询工具：%d 条 GB/T 3452.1 标准规格，支持内径/截面/外径查询、旧件实测值近似匹配、按温度与介质自动推荐材质并排除不适用材质。" % specs["meta"]["count"],
        "O型圈规格表,O型圈尺寸查询,O型圈材质选型,GB/T 3452.1,O型密封圈,密封件规格查询,氟橡胶丁腈橡胶",
        SITE_URL + "/", body, "website", ld)


def build_tool():
    tpl = read(os.path.join(TPL, "tool.html"))
    specs = json.loads(read(os.path.join(DATA, "o-ring-specs.json")))
    mats = json.loads(read(os.path.join(DATA, "materials.json")))
    media = json.loads(read(os.path.join(DATA, "media.json")))
    payload = {
        "specs": specs["specs"],
        "materials": mats["materials"],
        "media": media["media"],
    }
    data_js = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    html = tpl.replace("/*__SEAL_DATA__*/", data_js)
    assert "__SEAL_DATA__" not in html, "数据注入失败"
    write("tool/index.html", html)
    return specs["meta"]["count"]


def build_lists(articles):
    mats = [a for a in articles if a.get("category") == "materials"]
    arts = [a for a in articles if a.get("category") != "materials"]

    def list_page(title, h1, sub, items, canonical, desc, kw):
        body = """
<section class="tight">
  <div class="wrap">
    <div class="crumb" style="font-size:13px;color:var(--ink-3);margin:16px 0 10px"><a href="/">首页</a> / %s</div>
    <h2 class="sec">%s</h2>
    <p class="sub">%s</p>
    <div class="alist">
      %s
    </div>
  </div>
</section>
""" % (h1, h1, sub, "\n      ".join(article_card(a) for a in items))
        ld = jsonld({"@context": "https://schema.org", "@type": "CollectionPage", "name": h1,
                     "url": canonical, "inLanguage": "zh-CN"})
        return render_layout(title, desc, kw, canonical, body, "website", ld)

    write("materials/index.html", list_page(
        "O型圈材质百科 | NBR、FKM、EPDM 性能与耐介质对照 - " + DOMAIN_CN,
        "材质百科",
        "把每种材质的耐温边界、耐受介质、明确禁区和替代方案讲清楚。选材质的核心不是记名字，而是记住它们各自的禁区。",
        mats, SITE_URL + "/materials/",
        "O 型圈常用材质详解：丁腈橡胶 NBR、氟橡胶 FKM、三元乙丙 EPDM 的耐温范围、耐介质清单、不耐介质与替代选材建议。",
        "O型圈材质,NBR材质,FKM氟橡胶,EPDM三元乙丙,O型圈材料对照"))

    write("articles/index.html", list_page(
        "O型圈技术文章 | 规格读法、压缩率、标准对照、失效分析 - " + DOMAIN_CN,
        "技术文章",
        "从规格表示法到沟槽设计，从标准互换到失效反推，都是现场真会遇到的问题。",
        arts, SITE_URL + "/articles/",
        "O 型圈技术文章合集：规格代号怎么读、压缩率与沟槽设计、GB/JIS/AS568 标准对照与互换判断、常见失效模式与排查顺序。",
        "O型圈技术文章,O型圈压缩率,O型圈标准对照,O型圈失效原因"))


def build_articles(articles):
    for a in articles:
        body_html = to_html(a["body_md"])
        others = [x for x in articles if x["slug"] != a["slug"]
                  and x.get("category") == a.get("category")][:4]
        rel = ""
        if others:
            rel = ('<div class="rel"><h3>相关阅读</h3><ul>%s</ul></div>' %
                   "".join('<li><a href="/articles/%s/">%s</a></li>' % (o["slug"], o["title"]) for o in others))
        body = """
<article class="article" style="margin:26px 0">
  <div class="wrap" style="padding:0">
    <div class="crumb" style="max-width:820px;margin:0 auto 14px"><a href="/">首页</a> / <a href="/%s/">%s</a> / 正文</div>
    <div style="max-width:820px;margin:0 auto">
      <h1>%s</h1>
      <div class="meta">%s　·　%s</div>
      %s
      <div class="cta">
        <h3>需要按你的实际工况定材质或规格？</h3>
        <p>用工具输入温度与介质，可以直接看到推荐材质与被排除材质的原因；也可以把工况发给我们做一对一的选型确认。</p>
        <a class="btn solid" href="/tool/" style="margin-right:10px">打开选型工具</a>
        <a class="btn solid" href="/contact/">提交工况咨询</a>
      </div>
      %s
    </div>
  </div>
</article>
""" % ("materials" if a.get("category") == "materials" else "articles",
       a.get("category_name", ""), a["title"],
       a.get("date", BUILD_TIME), a.get("category_name", ""),
       body_html, rel)
        ld = jsonld({
            "@context": "https://schema.org", "@type": "Article",
            "headline": a["title"], "description": a["desc"],
            "datePublished": a.get("date", BUILD_TIME), "dateModified": a.get("date", BUILD_TIME),
            "inLanguage": "zh-CN", "author": {"@type": "Organization", "name": DOMAIN_CN},
            "publisher": {"@type": "Organization", "name": DOMAIN_CN},
            "mainEntityOfPage": "%s/articles/%s/" % (SITE_URL, a["slug"]),
        })
        write("articles/%s/index.html" % a["slug"], render_layout(
            a["title"] + " - " + DOMAIN_CN, a["desc"], a.get("keywords", ""),
            "%s/articles/%s/" % (SITE_URL, a["slug"]), body, "article", ld))


FAQ = [
    ("O 型圈规格 20×2.65 是什么意思？",
     "第一个数字是内径 d1 = 20 mm，第二个数字是截面直径（线径）d2 = 2.65 mm。外径不需要标出，按 外径 = 内径 + 2×截面 计算，即 20 + 2×2.65 = 25.3 mm。"),
    ("O 型圈的外径为什么不直接标出来？",
     "因为 O 型圈是弹性体，外径由内径与截面推导得出。GB/T 3452.1-2005 只规定内径与截面这两个基本尺寸及其公差，所以没有单独的“国标外径表”，外径是计算值。"),
    ("怎么从旧件测出的尺寸找到标准规格？",
     "用本站[近似匹配功能](/tool/)输入实测内径与实测截面，系统按匹配度排序给出前 12 个候选。注意实测内径通常略小于原始尺寸，若结果卡在两个规格之间，优先选内径略大的一侧。"),
    ("液压油用什么材质的 O 型圈？",
     "常温下用丁腈橡胶 NBR 即可；温度到 100~150℃ 用氢化丁腈 HNBR；150~200℃ 用氟橡胶 FKM。要特别注意：如果“液压油”是磷酸酯型抗燃液压油，只能用 EPDM，NBR 会被溶解。"),
    ("氟橡胶 FKM 能不能用在蒸汽或热水上？",
     "不能。FKM 抗高温油、抗高温空气很好，但高温水或蒸汽会使其脱氟降解。蒸汽与热水工况应选 EPDM 或蒸汽专用牌号，口诀是“FKM 怕水不怕油”。"),
    ("EPDM 能不能用在液压油里？",
     "绝对不能。EPDM 属非极性橡胶，遇到矿物系油品会迅速溶胀，体积膨胀可达 30% 以上。这是现场最常见的选型错误之一：EPDM 耐水耐候很强，但见油即废。"),
    ("硅橡胶耐温 200℃，为什么不能用在液压系统？",
     "硅橡胶耐温宽、耐候好，但耐矿物油性能差，会明显溶胀且强度下降。高温液压场合是双重不利，应改用 FKM 或 HNBR。"),
    ("国标 O 型圈能直接替换进口的 AS568 件吗？",
     "不能直接互换。AS568 的截面是英制换算值（如 1/8\" = 3.175 mm），与国标 3.55 mm 差 0.375 mm，会直接改变压缩率。截面偏差超过 0.2 mm 就应重新核算沟槽或按原标准采购。"),
    ("O 型圈压缩率取多少合适？",
     "静态端面密封 20%~25%，静态径向密封 15%~20%，往复动态密封 12%~18%，旋转密封 8%~12%。动得越快，压缩率应越小，因为摩擦热会加速老化。"),
    ("密封圈膨胀变胖是什么原因？",
     "材质与介质不兼容导致的溶胀。常见组合：EPDM 接触矿物油、硅橡胶接触油或燃油、丁腈接触酮类或酯类、氟橡胶接触低分子酯。正确做法是换材质，而不是加大沟槽。"),
]


def build_faq():
    items = "\n".join(
        '<div class="card" style="margin-bottom:14px"><h3>%s</h3><p>%s</p></div>' % (q, a)
        for q, a in FAQ)
    # FAQ 里的 markdown 链接转成 HTML 链接
    items = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', items)
    body = """
<section class="tight">
  <div class="wrap">
    <div class="crumb" style="font-size:13px;color:var(--ink-3);margin:16px 0 10px"><a href="/">首页</a> / 常见问题</div>
    <h2 class="sec">O 型圈常见问题</h2>
    <p class="sub">规格读法、材质选择、压缩率、标准互换、失效判断——最常见的十个问题，直接给结论。</p>
    <div style="max-width:860px">
    %s
    </div>
  </div>
</section>
""" % items
    ld = jsonld({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ],
    })
    write("faq/index.html", render_layout(
        "O型圈常见问题解答 | 规格、材质、压缩率、标准互换 - " + DOMAIN_CN,
        "O 型圈十个高频问题：规格代号怎么读、外径怎么算、液压油选什么材质、氟橡胶能不能用在蒸汽上、压缩率取多少、密封圈变胖是什么原因。",
        "O型圈常见问题,O型圈怎么选,O型圈材质,密封圈问题",
        SITE_URL + "/faq/", body, "website", ld))


def build_contact():
    tpl = read(os.path.join(TPL, "contact.html"))
    if FEISHU_WEBHOOK:
        mode, target = "webhook", FEISHU_WEBHOOK
    elif FORM_ENDPOINT:
        mode, target = "worker", FORM_ENDPOINT
    else:
        mode, target = "off", ""
    cfg_js = json.dumps({
        "mode": mode,
        "webhook": FEISHU_WEBHOOK,
        "worker": FORM_ENDPOINT,
        "keyword": FEISHU_KEYWORD,
        "site": DOMAIN_CN,
    }, ensure_ascii=False)
    body = tpl.replace("/*__FORM_CFG__*/", cfg_js)
    assert "__FORM_CFG__" not in body, "表单配置注入失败"
    ld = jsonld({"@context": "https://schema.org", "@type": "ContactPage",
                 "name": "选型咨询与报价", "url": SITE_URL + "/contact/", "inLanguage": "zh-CN"})
    write("contact/index.html", render_layout(
        "O型圈选型咨询与报价 | 提供工况即可定材质与规格 - " + DOMAIN_CN,
        "提交 O 型圈工况（温度、介质、压力、尺寸、数量），获取材质、规格、硬度与用量建议及报价。",
        "O型圈报价,O型圈选型咨询,密封圈定制,O型圈询价",
        SITE_URL + "/contact/", body, "website", ld))
    label = {"webhook": "飞书群机器人（浏览器直连）",
             "worker": "Cloudflare Worker 中转",
             "off": "未配置 → 演示模式（不向第三方发送）"}[mode]
    print("询单接收端：%s%s" % (label, ("  " + target) if target else ""))
    return mode



def build_about():
    body = """
<section class="tight">
  <div class="wrap">
    <div class="crumb" style="font-size:13px;color:var(--ink-3);margin:16px 0 10px"><a href="/">首页</a> / 关于</div>
    <h2 class="sec">关于本站</h2>
    <p class="sub">密封件.cn 是一个专注 O 型密封圈的规格与选型参考资料站。</p>
    <div style="max-width:820px">
      <div class="card" style="margin-bottom:16px">
        <h3>这个站解决什么问题</h3>
        <p>O 型圈是个小零件，但选型牵扯四件事：尺寸、公差、材质、沟槽。市面上的资料要么是一张看不懂的规格 PDF，要么是只有厂家才知道的口径。本站做三件事：把国标规格数字化成可查询的数据；把材质耐介质规则整理成可计算的逻辑；把现场真正会踩的坑写成能看懂的文章。</p>
      </div>
      <div class="card" style="margin-bottom:16px">
        <h3>数据来源与口径</h3>
        <ul>
          <li>规格尺寸：GB/T 3452.1-2005《液压气动用O形橡胶密封圈 第1部分：尺寸系列及公差》，等同采用 ISO 3601-1，取 G 系列（一般应用）。</li>
          <li>外径按 d3 = d1 + 2×d2 计算，公差为标称值。</li>
          <li>材质耐介质结论为工程经验归纳，用于快速初筛，不替代浸泡试验。</li>
        </ul>
      </div>
      <div class="card">
        <h3>免责声明</h3>
        <p>本站内容用于设计选型与采购比对的参考。密封件实际性能受配方、工艺、批次、安装与工况波动影响，正式定型前请以厂家实测报告、介质相容性试验及标准原文为准。因使用本站内容造成的直接或间接损失，本站不承担责任。</p>
      </div>
    </div>
  </div>
</section>
"""
    write("about/index.html", render_layout(
        "关于本站 | " + DOMAIN_CN + " O型圈规格查询与选型参考",
        "密封件.cn 专注 O 型圈规格查询与材质选型：数据来源、计算口径、使用边界与免责说明。",
        "密封件.cn,O型圈规格查询,关于本站",
        SITE_URL + "/about/", body, "website", ""))


def build_404():
    body = """
<section class="tight">
  <div class="wrap" style="text-align:center;padding:60px 0 80px">
    <h2 class="sec" style="font-size:44px;margin-bottom:6px">404</h2>
    <p class="sub" style="margin:0 auto 26px;max-width:520px">这个页面不存在。可能是链接输错了，或者页面已经调整位置。</p>
    <p>
      <a class="btn solid" href="/">回首页</a>
      <a class="btn solid" style="margin-left:10px" href="/tool/">规格查询工具</a>
    </p>
  </div>
</section>
"""
    write("404.html", render_layout("页面不存在 - " + DOMAIN_CN, "页面不存在。", "", SITE_URL + "/404.html", body))


def build_seo(articles):
    urls = ["/", "/tool/", "/materials/", "/articles/", "/faq/", "/contact/", "/about/"]
    urls += ["/articles/%s/" % a["slug"] for a in articles]
    today = datetime.date.today().isoformat()
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        pri = "1.0" if u == "/" else ("0.9" if u in ("/tool/",) else "0.7")
        sm.append("  <url><loc>%s%s</loc><lastmod>%s</lastmod><changefreq>weekly</changefreq><priority>%s</priority></url>"
                  % (SITE_URL, u, today, pri))
    sm.append("</urlset>\n")
    write("sitemap.xml", "\n".join(sm))

    write("robots.txt",
          "# 密封件.cn\n"
          "User-agent: *\n"
          "Allow: /\n"
          "Disallow: /data/\n"
          "\n"
          "# 百度/必应/谷歌等主流爬虫均允许抓取\n"
          "Sitemap: %s/sitemap.xml\n" % SITE_URL)

    # GitHub Pages 自定义域名
    write("CNAME", DOMAIN_ASCII + "\n")

    # GitHub Actions 自动部署（纯静态，直接发布 public/）
    wf = """name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/checkout@v4
      - name: 构建站点
        # 询单接收端：在仓库 Settings → Secrets and variables → Actions 里
        # 添加 FEISHU_WEBHOOK（可选 FEISHU_KEYWORD），即可不写死进代码
        env:
          SEAL_FEISHU_WEBHOOK: ${{ secrets.FEISHU_WEBHOOK }}
          SEAL_FEISHU_KEYWORD: ${{ secrets.FEISHU_KEYWORD }}
        run: |
          python -m pip install --quiet markdown idna
          python build.py
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with:
          path: public
      - id: deployment
        uses: actions/deploy-pages@v4
"""
    # 工作流必须位于【仓库根】目录才生效，且不属于站点产物，故写到 BASE 而非 PUB
    wfdir = os.path.join(BASE, ".github", "workflows")
    os.makedirs(wfdir, exist_ok=True)
    with open(os.path.join(wfdir, "deploy.yml"), "w", encoding="utf-8") as f:
        f.write(wf)


def main():
    # 覆盖式构建：不删除整个 public/（避免与本地预览服务/系统回收站策略冲突）
    os.makedirs(PUB, exist_ok=True)

    # 校验域名 punycode
    try:
        import idna
        dec = idna.decode(DOMAIN_ASCII)
        assert dec == DOMAIN_CN, "punycode 不匹配: %s -> %s" % (DOMAIN_ASCII, dec)
        print("域名校验通过：%s -> %s" % (DOMAIN_ASCII, DOMAIN_CN))
    except ImportError:
        print("（未安装 idna，跳过 punycode 校验）")

    articles = parse_content()
    print("内容文章：%d 篇" % len(articles))

    # 静态资源：static/ 下所有文件原样复制到 public/ 根
    # 搜索引擎验证文件（BingSiteAuth.xml 等）、图片、字体都放 static/，构建后自动带到站点根目录
    n_static = 0
    for dirpath, _, filenames in os.walk(STATIC):
        for fn in filenames:
            if fn.startswith("."):
                continue
            src = os.path.join(dirpath, fn)
            rel = os.path.relpath(src, STATIC)
            dst = os.path.join(PUB, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy(src, dst)
            n_static += 1
    print("静态资源：%d 个文件" % n_static)
    os.makedirs(PUB_DATA, exist_ok=True)
    for fn in os.listdir(DATA):
        if fn.endswith(".json"):
            shutil.copy(os.path.join(DATA, fn), os.path.join(PUB_DATA, fn))

    n = build_tool()
    print("工具页数据注入：%d 条规格" % n)
    write("index.html", build_home(articles))
    build_lists(articles)
    build_articles(articles)
    build_faq()
    build_contact()
    build_about()
    build_404()
    build_seo(articles)

    # 统计
    total = 0
    for root, dirs, files in os.walk(PUB):
        for f in files:
            total += 1
    print("构建完成：public/ 共 %d 个文件" % total)
    for root, dirs, files in os.walk(PUB):
        rel = os.path.relpath(root, PUB).replace("\\", "/")
        for f in sorted(files):
            if f.endswith(".html") or f in ("robots.txt", "sitemap.xml", "CNAME"):
                print("  %s" % (("%s/%s" % (rel, f)).lstrip("./")))


if __name__ == "__main__":
    main()
