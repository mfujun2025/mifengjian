/**
 * 密封件.cn 询单表单 → 飞书群机器人 中转 Worker
 *
 * 作用：把 webhook 地址藏在服务端，前端只暴露自己的域名。
 *      比前端直连飞书多出：防刷、字段裁剪、真实回执、webhook 不泄露。
 *
 * 部署（Cloudflare Workers）：
 *   1. Cloudflare Dashboard → Workers & Pages → 创建 Worker
 *   2. 把本文件内容整体粘进去，保存并部署
 *   3. Settings → Variables → 添加环境变量（加密）：
 *        FEISHU_WEBHOOK = https://open.feishu.cn/open-apis/bot/v2/hook/你的token
 *      （可选）ALLOW_ORIGINS = https://xn--5nq252acf.cn,https://www.xn--5nq252acf.cn
 *   4. 部署得到的地址形如 https://xxx.yyy.workers.dev，填进 build.py 的 FORM_ENDPOINT
 *
 * 免费额度：10 万次请求/天，询单场景完全用不完。
 */

const DEFAULT_ORIGINS = [
  "https://xn--5nq252acf.cn",
  "https://www.xn--5nq252acf.cn",
  "http://127.0.0.1:8791",
  "http://localhost:8791",
];

// 轻量防刷：同一 isolate 内按 IP 计数（无状态环境，重启即清，用于挡脚本刷）
const HITS = new Map();
const WINDOW_MS = 60 * 1000;
const MAX_PER_WINDOW = 5;

function corsHeaders(origin, allowed) {
  const ok = allowed.includes(origin) || allowed.includes("*");
  return {
    "Access-Control-Allow-Origin": ok ? origin : allowed[0],
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "content-type",
    "Access-Control-Max-Age": "86400",
    Vary: "Origin",
  };
}

function json(body, status, origin, allowed) {
  return new Response(JSON.stringify(body), {
    status: status || 200,
    headers: Object.assign({ "Content-Type": "application/json; charset=utf-8" }, corsHeaders(origin, allowed)),
  });
}

function clip(v, n) {
  return String(v == null ? "" : v).trim().slice(0, n);
}

export default {
  async fetch(request, env) {
    const allowed = (env.ALLOW_ORIGINS ? env.ALLOW_ORIGINS.split(",").map((s) => s.trim()) : DEFAULT_ORIGINS);
    const origin = request.headers.get("Origin") || "";

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: corsHeaders(origin, allowed) });
    }
    if (request.method !== "POST") {
      return json({ ok: false, error: "method not allowed" }, 405, origin, allowed);
    }
    if (origin && !allowed.includes(origin) && !allowed.includes("*")) {
      return json({ ok: false, error: "origin not allowed" }, 403, origin, allowed);
    }

    // 限流
    const ip = request.headers.get("CF-Connecting-IP") || "unknown";
    const now = Date.now();
    const rec = HITS.get(ip);
    if (!rec || now - rec.t0 > WINDOW_MS) {
      HITS.set(ip, { t0: now, n: 1 });
    } else if (++rec.n > MAX_PER_WINDOW) {
      return json({ ok: false, error: "too many requests, 请稍后再试" }, 429, origin, allowed);
    }
    if (HITS.size > 5000) HITS.clear();

    let data;
    try {
      data = await request.json();
    } catch (e) {
      return json({ ok: false, error: "invalid json" }, 400, origin, allowed);
    }

    // 蜜罐
    const p = (data && data.payload) || {};
    if (clip(p.company_url, 100)) {
      return json({ ok: true, note: "dropped" }, 200, origin, allowed);
    }

    const keyword = clip(data.keyword, 20) || "询单";
    const site = clip(data.site, 40) || "密封件.cn";
    const FIELDS = [
      ["称呼", "name", 40],
      ["联系方式", "contact", 60],
      ["规格/尺寸", "size", 60],
      ["数量", "qty", 40],
      ["工作温度", "temp", 40],
      ["接触介质", "media", 60],
      ["补充说明", "note", 800],
    ];
    const lines = FIELDS
      .map(([label, key, max]) => {
        const v = clip(p[key], max);
        return v ? `**${label}**：${v.replace(/[<>]/g, "")}` : "";
      })
      .filter(Boolean);

    if (!lines.length) {
      return json({ ok: false, error: "empty payload" }, 400, origin, allowed);
    }

    const ts = new Date(Date.now() + 8 * 3600 * 1000).toISOString().replace("T", " ").slice(0, 16);
    const card = {
      msg_type: "interactive",
      card: {
        config: { wide_screen_mode: true },
        header: { template: "blue", title: { tag: "plain_text", content: `\uD83D\uDD14 新${keyword} · ${site}` } },
        elements: [
          { tag: "div", text: { tag: "lark_md", content: lines.join("\n") } },
          { tag: "hr" },
          { tag: "note", elements: [{ tag: "plain_text", content: `来源：${site} 选型咨询页 · ${ts} · 类型：${keyword}` }] },
        ],
      },
    };

    let fr, fj;
    try {
      fr = await fetch(env.FEISHU_WEBHOOK, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(card),
      });
      fj = await fr.json();
    } catch (e) {
      return json({ ok: false, error: "upstream failed: " + e.message }, 502, origin, allowed);
    }

    if (fj && (fj.code === 0 || fj.StatusCode === 0)) {
      return json({ ok: true }, 200, origin, allowed);
    }
    return json({ ok: false, error: (fj && (fj.msg || fj.StatusMessage)) || "feishu rejected" }, 502, origin, allowed);
  },
};
