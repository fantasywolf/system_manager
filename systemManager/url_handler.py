import os
import subprocess
import sys

from django.http import JsonResponse
from django.middleware.csrf import get_token


def start_monitor(request):
    res = subprocess.run('ps -e | grep collect_metrics | grep -v grep', shell=True,capture_output=True)
    print(f"res.stdout={res.stdout}")
    if res.stdout != b'' :
        return JsonResponse({'status': 'task is running'})
    else:
        res = subprocess.run(f"{sys.executable} manage.py collect_metrics --interval 3 &",
                             shell=True)
        if res.returncode == 0:
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'not ok'})


def stop_monitor(request):
    res = subprocess.run("kill `ps -e | grep collect_metrics | grep -v grep | cut -d ' ' -f1`",
                         shell=True)
    if res.returncode == 0:
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'not ok'})


def get_csrf_token(request):
    token = get_token(request)  # Django自动生成Token并设置Cookie
    return JsonResponse({'csrf_token': token})
