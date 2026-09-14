# -*- coding: utf-8 -*-
"""生成询单表单的自动化验证页 public/_t_form.html（用完即删）。
用法：?c=ok|fail|honeypot|required|prefill|real"""
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "public", "contact", "index.html")
OUT = os.path.join(ROOT, "public", "_t_form.html")

AUTO = r"""
<pre id="tresult">PENDING</pre>
<script>
(function(){
  var C = new URLSearchParams(location.search).get('c') || 'ok';
  function set(id, v){ var e = document.getElementById(id); if(e) e.value = v; }
  function finish(o){
    var d = document.getElementById('tresult');
    d.textContent = 'RESULT:' + JSON.stringify(o);
  }
  window.addEventListener('load', function(){
    var cfg = window.__RF__.cfg;
    if(C !== 'required'){
      set('c1', C === 'fail' ? 'FAILTEST客户' : '张工程师');
      set('c2', '13800138000');
    }
    if(C !== 'required' && C !== 'prefill'){
      set('c3', '20×2.65');
      set('c4', '500 只/月');
      set('c5', '长期 120，峰值 150');
      set('c6', '矿物液压油');
      set('c7', '压力 16MPa，往复运动，需要耐油认证');
    }
    if(C === 'honeypot') set('c9', 'http://spam.example/robot');
    if(C === 'real') cfg.webhook = 'https://open.feishu.cn/open-apis/bot/v2/hook/00000000-0000-0000-0000-000000000000';

    window.__RF__.submit();

    var n = 0;
    var iv = setInterval(function(){
      n++;
      var ok = document.getElementById('ok').classList.contains('on');
      var err = document.getElementById('err').classList.contains('on');
      if(ok || err || n > 80){
        clearInterval(iv);
        finish({
          c: C,
          okShown: ok, errShown: err,
          errTitle: document.getElementById('errtitle').textContent,
          errMsg: document.getElementById('errmsg').textContent.slice(0, 180),
          okList: document.getElementById('oklist').textContent.slice(0, 300),
          sizeVal: document.getElementById('c3').value,
          mediaVal: document.getElementById('c6').value,
          tempVal: document.getElementById('c5').value,
          fillTip: document.getElementById('filltip').classList.contains('on'),
          cfgMode: cfg.mode,
          hook: cfg.webhook
        });
      }
    }, 60);
  });
})();
</script>
"""

html = io.open(SRC, encoding="utf-8").read()
html = html.replace("</body>", AUTO + "\n</body>")
if "</body>" not in io.open(SRC, encoding="utf-8").read():
    html = html + AUTO
io.open(OUT, "w", encoding="utf-8", newline="\n").write(html)
print("生成", OUT)
