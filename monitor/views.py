# Create your views here.
import subprocess
import sys

from django.http import JsonResponse
from django.middleware.csrf import get_token

from monitor.models import SystemMetrics


def start_monitor(request):
    res = subprocess.run('ps -ef | grep collect_metrics | grep -v grep', shell=True, capture_output=True)
    if res.stdout != b'':
        return JsonResponse({'status': 'task is running'})
    else:
        res = subprocess.run(f"{sys.executable} manage.py collect_metrics --interval 3 &",
                             shell=True)
        if res.returncode == 0:
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'not ok'})


def stop_monitor(request):
    res = subprocess.run("kill `ps -e | tr -s ' ' |  grep collect_metrics | grep -v grep | cut -d ' ' -f1`",
                         shell=True)
    if res.returncode == 0:
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'not ok'})


# 概览接口 获取 cpu 内存 磁盘 网络的 总体数据
def overview(request):
    data = SystemMetrics.objects.latest('timestamp')
    return JsonResponse({'cpu_usage': data.cpu_usage,
                         'mem_usage': data.mem_usage,
                         'disk_usage': data.disk_usage,
                         'net_recv': data.net_recv,
                         'net_sent': data.net_sent, })


# cpu详情数据：cpu每个内核的使用率，
def cpu_detail(request):
    data = SystemMetrics.objects.latest('timestamp')
    return JsonResponse({'cpu_usage': data.cpu_usage,
                         'cpu_load_1': data.cpu_load_1,
                         'cpu_load_5': data.cpu_load_5,
                         'cpu_load_15': data.cpu_load_15, })


# 内存的详情数据： 内存已使用了 ， 未使用，可获取的...
def mem_detail(request):
    data = SystemMetrics.objects.latest('timestamp')
    return JsonResponse({'mem_usage': data.mem_usage,
                         'mem_total': data.mem_total,
                         'mem_free': data.mem_free,
                         'mem_used': data.mem_used, })


# disk详情数据：有多少个分区，每个分区多少兆， 使用率
def disk_detail(request):
    data = SystemMetrics.objects.latest('timestamp')
    return JsonResponse({'disk_usage': data.disk_usage,
                         'disk_total': data.disk_total,
                         'disk_free': data.disk_free,
                         'disk_used': data.disk_used, })


# 网络数据获取
def net_detail(request):
    data = SystemMetrics.objects.latest('timestamp')
    return JsonResponse({'net_recv': data.net_recv,
                         'net_sent': data.net_sent, })
