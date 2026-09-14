# -*- coding: utf-8 -*-
"""
密封件.cn —— 询单接收端一键配置

干什么：
  1. 接收你的飞书群自定义机器人 webhook 地址
  2. 校验格式、真发一条测试卡片到群里（你可以立刻在飞书看到）
  3. 写入 config.local.json
  4. 自动重建站点，把配置注入 public/contact/index.html

怎么用：双击同目录下的「配置询单接收端.bat」，或在本目录执行
      python setup_form.py
"""
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
CFG_PATH = os.path.join(BASE, "config.local.json")
BUILD = os.path.join(BASE, "build.py")

HOOK_RE = re.compile(r"^https://open\.feishu\.cn/open-apis/bot/v2/hook/[A-Za-z0-9_\-]+$")
WORKER_RE = re.compile(r"^https://[A-Za-z0-9\.\-]+(\.workers\.dev)?/?$")

LINE = "-" * 66

# 飞书返回的常见错误码，见过就懂
ERR_HINT = {
    19001: "webhook 地址无效 —— 多半是复制时少了尾巴，或这个机器人已经被删掉了",
    19024: "关键词校验失败 —— 把安全设置里的关键词改成「询单」，或与下面填的保持一致",
    19022: "IP 白名单校验失败 —— 纯静态站不能用这项（出口 IP 不固定），请改成自定义关键词",
    19021: "签名校验失败 —— 纯静态站没有后端，不能开签名，请改成自定义关键词",
    9499: "请求体格式错误",
    11232: "触发限流（单机器人 100 次/分钟）",
}


def load_cfg():
    if os.path.isfile(CFG_PATH):
        try:
            with open(CFG_PATH, encoding="utf-8") as f:
                return json.load(f) or {}
        except Exception:
            pass
    return {}


def save_cfg(cfg):
    with open(CFG_PATH, "w", encoding="utf-8", newline="\n") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
        f.write("\n")


def test_card(keyword):
    """一张和网站真实询单格式一致的测试卡片。"""
    return {
        "msg_type": "interactive",
        "card": {
            "config": {"wide_screen_mode": True},
            "header": {
                "template": "blue",
                "title": {"tag": "plain_text", "content": "🔔 新询单 · 密封件.cn（通道自检）"},
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": (
                            "**称呼**：张工程师\n"
                            "**联系方式**：13800138000\n"
                            "**规格/尺寸**：20×2.65\n"
                            "**数量**：500 只/月\n"
                            "**工作温度**：长期 120，峰值 150\n"
                            "**接触介质**：矿物液压油\n"
                            "**补充说明**：这是一条通道自检消息。你能看到它，就说明询单通道已经打通。"
                        ),
                    },
                },
                {"tag": "hr"},
                {
                    "tag": "note",
                    "elements": [
                        {"tag": "plain_text", "content": "类型：询单 · 配置自检 · 并未来自真实访客"}
                    ],
                },
            ],
        },
    }


def post_json(url, payload, timeout=15):
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")
    except Exception as e:
        return None, str(e)


def main():
    print(LINE)
    print(" 密封件.cn · 询单接收端配置")
    print(LINE)
    cfg = load_cfg()
    cur = cfg.get("feishu_webhook", "")
    if cur:
        print("当前已配置：%s…%s" % (cur[:58], cur[-6:]))
    else:
        print("当前未配置（表单处于演示模式：只校验、不发送）")
    print()
    print("【没有 webhook？】照着做，1 分钟：")
    print("  1. 打开飞书，进入「密封件.cn 询单」群（已经给你建好了，只有你一个人）")
    print("  2. 点右上角 ··· → 设置 → 群机器人 → 添加机器人 → 选「自定义机器人」")
    print("  3. 名字填「密封件.cn 询单」→ 添加")
    print("  4. 安全设置里勾「自定义关键词」，关键词填：询单   ← 千万别选签名/IP 白名单")
    print("  5. 复制 webhook 地址（https://open.feishu.cn/open-apis/bot/v2/hook/...）")
    print()

    raw = input("把 webhook 地址粘到这里（直接回车=清空改回演示模式）：").strip()
    if not raw:
        cfg["feishu_webhook"] = ""
        save_cfg(cfg)
        print("\n已清空配置。重建站点…\n")
        subprocess.run([sys.executable, BUILD], cwd=BASE)
        print("\n完成：表单回到演示模式（不向任何第三方发送数据）。")
        return

    url = raw.split("?")[0].rstrip("/")
    if not HOOK_RE.match(url):
        print("\n[×] 这不像飞书自定义机器人的 webhook。")
        print("    正确格式：https://open.feishu.cn/open-apis/bot/v2/hook/一长串字符")
        print("    你粘的是：%s" % raw[:100])
        print("    注意别把机器人详情页的网址粘过来 —— 要的是 webhook 地址本身。")
        return

    kw = input("安全设置里的自定义关键词（直接回车=询单）：").strip() or "询单"

    print("\n正在向飞书发一条测试卡片…")
    status, body = post_json(url, test_card(kw))
    print("  HTTP %s" % status)
    print("  响应：%s" % body.strip()[:300])

    ok = False
    try:
        r = json.loads(body)
        code = r.get("code", r.get("StatusCode"))
        ok = code == 0
    except Exception:
        code = None

    if ok:
        print("\n[√] 发送成功 —— 去飞书「密封件.cn 询单」群看那条卡片吧。")
    else:
        hint = ERR_HINT.get(code)
        print("\n[×] 飞书拒绝了这条消息。")
        if hint:
            print("    原因：%s" % hint)
        print("    这一步没过就先别往下走，改好群里的安全设置再重跑本脚本。")
        if input("\n仍然要保存当前地址吗？(y/N)：").strip().lower() != "y":
            print("已放弃，配置未改动。")
            return

    cfg["feishu_webhook"] = url
    cfg["feishu_keyword"] = kw
    cfg.setdefault("form_endpoint", "")
    save_cfg(cfg)
    print("\n配置已写入 %s" % CFG_PATH)
    print("重建站点…\n")
    subprocess.run([sys.executable, BUILD], cwd=BASE)

    print()
    print(LINE)
    print(" 搞定。接下来：")
    print("   本地看效果：cd public && python -m http.server 8791")
    print("               浏览器打开 http://127.0.0.1:8791/contact/")
    print("   真机走一遍：提交表单 → 飞书群里应立刻收到卡片")
    print(LINE)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n已取消，配置未改动。")
    except EOFError:
        print("\n输入中断，配置未改动。")
