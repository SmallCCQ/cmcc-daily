# -*- coding: utf-8 -*-
"""cmdb-daily Web 服务守护进程：定时健康检查，进程退出/崩溃自动重启。

用法：python cmcc_guard.py
- 每分钟检查 http://127.0.0.1:8080/healthz
- 不健康（连接失败/非200）就拉起 `python -m cmcc_app serve`
- 日志写到 guard.log
"""
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent
PORT = 8080
CHECK_INTERVAL = 60
HEALTH_URL = f"http://127.0.0.1:{PORT}/healthz"
PYTHON = r"C:\Users\Smallsun\AppData\Local\Programs\Python\Python312\python.exe"

def log(msg):
    line = time.strftime("%Y-%m-%d %H:%M:%S") + " " + msg
    print(line, flush=True)
    with open(BASE / "guard.log", "a", encoding="utf-8") as f:
        f.write(line + "\n")

def healthy() -> bool:
    try:
        with urllib.request.urlopen(HEALTH_URL, timeout=5) as r:
            return r.status == 200
    except Exception:
        return False

def launch():
    log("拉起 cmcc_app serve ...")
    kwargs = {}
    if sys.platform == "win32":
        kwargs["creationflags"] = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    import os
    env = dict(os.environ)
    env["CMCC_BIND"] = "0.0.0.0"
    env["CMCC_PORT"] = "8080"
    subprocess.Popen(
        [PYTHON, "-m", "cmcc_app", "serve"],
        cwd=str(BASE),
        env=env,
        stdout=open(BASE / "web.log", "a", encoding="utf-8"),
        stderr=subprocess.STDOUT,
        **kwargs,
    )

def main():
    log("守护进程启动，监控 " + HEALTH_URL)
    while True:
        if not healthy():
            log("检测到服务不健康，重启中 ...")
            launch()
            time.sleep(8)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
