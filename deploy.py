# -*- coding: utf-8 -*-
"""发布更新到线上 —— 密封件.cn

  python deploy.py              构建产物 -> gh-pages 分支（Pages 从这里发布）
  python deploy.py --source     同时把源码 -> main 分支
  python deploy.py --check      只查看状态，不推送

为什么不用 git push：本机网络加速工具会拦截 git 的网络子进程，
因此改为直接调用 GitHub REST API 上传（效果等同，只是少了本地 .git 目录）。
"""
import base64
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.request

REPO = "mfujun2025/mifengjian"
PAGES_BRANCH = "gh-pages"
SOURCE_BRANCH = "main"
CNAME = "xn--5nq252acf.cn"

BASE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(BASE, "public")

# 源码推送时跳过：产物目录、本地配置、部署脚本
TOP_SKIP = {".git", "public", "_deploy", "__pycache__", ".github", "runs"}
FILE_SKIP = {"config.local.json", ".DS_Store", "Thumbs.db"}

_ctx = ssl.create_default_context()
_ctx.check_hostname = False
_ctx.verify_mode = ssl.CERT_NONE


# ------------------------------------------------------------------ 凭据与请求
def token():
    """从 ~/.git-credentials 读取 GitHub token（只用不打印、不落盘）。"""
    path = os.path.expanduser("~/.git-credentials")
    if not os.path.exists(path):
        print("[x] 找不到凭据文件：%s" % path)
        print("    请先在本机对着任意 GitHub 仓库执行一次 git push，")
        print("    让 Windows 凭据管理器/ git 保存凭据后再运行本脚本。")
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if "github.com" in line and "@" in line:
                return line.split(":", 2)[2].split("@")[0]
    print("[x] 凭据文件里没有 github.com 的记录")
    sys.exit(1)


TOKEN = token()


def api(path, method="GET", data=None, timeout=40):
    url = path if path.startswith("http") else "https://api.github.com" + path
    body = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=body, method=method, headers={
        "Authorization": "Bearer " + TOKEN,
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "User-Agent": "seal-cn-deploy",
    })
    try:
        with urllib.request.urlopen(req, context=_ctx, timeout=timeout) as r:
            text = r.read().decode("utf-8", "replace")
            return r.status, (json.loads(text) if text.strip() else {})
    except urllib.error.HTTPError as e:
        text = e.read().decode("utf-8", "replace")
        try:
            return e.code, json.loads(text)
        except Exception:  # noqa: BLE001
            return e.code, text
    except Exception as e:  # noqa: BLE001
        return 0, str(e)


# ------------------------------------------------------------------ 文件收集
def collect(root, top_skip, file_skip):
    out = {}
    for dirpath, dirnames, filenames in os.walk(root):
        rel = os.path.relpath(dirpath, root).replace("\\", "/")
        rel = "" if rel == "." else rel
        if rel == "":
            dirnames[:] = [d for d in dirnames if d not in top_skip]
        for fn in filenames:
            relp = (rel + "/" + fn) if rel else fn
            if relp in file_skip or fn.endswith(".pyc"):
                continue
            out[relp] = os.path.join(dirpath, fn)
    return out


# ------------------------------------------------------------------ 上传流程
def get_head(branch):
    s, r = api("/repos/%s/git/ref/heads/%s" % (REPO, branch))
    return r["object"]["sha"] if s == 200 else None


def upload(files, branch, message, label):
    total = len(files)
    print("  上传 %d 个文件到 %s ..." % (total, branch))
    items = []
    for i, path in enumerate(sorted(files), 1):
        with open(files[path], "rb") as f:
            data = f.read()
        payload = {"content": base64.b64encode(data).decode(), "encoding": "base64"}
        for attempt in (1, 2, 3):
            s, r = api("/repos/%s/git/blobs" % REPO, "POST", payload)
            if s in (200, 201):
                items.append({"path": path, "mode": "100644", "type": "blob",
                              "sha": r["sha"]})
                break
            if s == 422 and attempt < 3:
                time.sleep(1)
                continue
            print("  [x] 失败：%s -> HTTP %s %s" % (path, s, str(r)[:150]))
            return None
        if i % 10 == 0 or i == total:
            print("    %s %d/%d" % (label, i, total))

    s, r = api("/repos/%s/git/trees" % REPO, "POST", {"tree": items})
    if s not in (200, 201):
        print("  [x] 建目录树失败：HTTP %s %s" % (s, str(r)[:200]))
        return None
    tree = r["sha"]

    head = get_head(branch)
    s, r = api("/repos/%s/git/commits" % REPO, "POST",
               {"message": message, "tree": tree, "parents": [head] if head else []})
    if s not in (200, 201):
        print("  [x] 建提交失败：HTTP %s %s" % (s, str(r)[:200]))
        return None
    sha = r["sha"]

    if head:
        s, r = api("/repos/%s/git/refs/heads/%s" % (REPO, branch), "PATCH",
                   {"sha": sha, "force": False})
    else:
        s, r = api("/repos/%s/git/refs" % REPO, "POST",
                   {"ref": "refs/heads/" + branch, "sha": sha})
    if s not in (200, 201):
        print("  [x] 更新分支失败：HTTP %s %s" % (s, str(r)[:200]))
        return None
    print("  %s -> %s" % (branch, sha[:8]))
    return sha


def wait_build(limit=10):
    print("  等待 GitHub Pages 构建", end="", flush=True)
    for _ in range(limit):
        s, r = api("/repos/%s/pages" % REPO)
        if s == 200 and r.get("status") == "built":
            print(" 完成")
            return True
        print(".", end="", flush=True)
        time.sleep(10)
    print(" 超时（可稍后到仓库 Actions 页查看）")
    return False


def show_status():
    s, r = api("/repos/%s/pages" % REPO)
    if s != 200:
        print("Pages 状态查询失败：HTTP %s %s" % (s, str(r)[:200]))
        return
    print("  线上地址：https://%s" % r.get("cname", CNAME))
    print("  部署分支：%s%s" % (r.get("source", {}).get("branch"),
                              r.get("source", {}).get("path")))
    print("  构建状态：%s" % r.get("status"))
    print("  强制 HTTPS：%s" % ("已开启" if r.get("https_enforced") else "未开启"))


def main():
    args = sys.argv[1:]
    check_only = "--check" in args
    with_source = "--source" in args

    print("=" * 56)
    print(" 密封件.cn  ->  github.com/%s" % REPO)
    print("=" * 56)

    if check_only:
        print("\n[本地]")
        print("  public/ 文件数：%d" % len(collect(PUB, set(), set())))
        print("\n[远端]")
        show_status()
        return

    # 1. 产物
    print("\n[1/2] 发布构建产物")
    files = collect(PUB, set(), set())
    if not files:
        print("  [x] public/ 是空的，请先运行：python build.py")
        sys.exit(1)
    if "index.html" not in files:
        print("  [x] public/ 里没有 index.html，构建不完整，已中止")
        sys.exit(1)
    if upload(files, PAGES_BRANCH, "发布：密封件.cn 站点更新", "产物") is None:
        sys.exit(1)

    # 2. 源码（可选）
    if with_source:
        print("\n[2/2] 同步源码到 main")
        src = collect(BASE, TOP_SKIP, FILE_SKIP)
        if upload(src, SOURCE_BRANCH, "站点源码更新", "源码") is None:
            sys.exit(1)
    else:
        print("\n[2/2] 源码未同步（加 --source 可一起推）")

    print("\n[部署]")
    wait_build()
    show_status()
    print("\n完成。站点：https://%s" % CNAME)
    print("若刚改过 DNS，证书签发后首次访问可能需 1~10 分钟。")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n已取消。")
