import subprocess
import re
import time


import psutil  # 需要安装: pip install psutil

import subprocess
import re
import time
import psutil
import platform



def get_cpu_info():
    """获取CPU信息"""
    try:
        # 根据操作系统使用不同的命令
        if platform.system() == 'Linux':
            # Linux 系统使用 top -bn1
            result = subprocess.run(['top', '-bn1'], stdout=subprocess.PIPE, text=True)
            output = result.stdout
            cpu_line = [line for line in output.split('\n') if '%Cpu(s)' in line][0]
            cpu_usage = 100 - float(re.findall(r'(\d+\.\d+) id', cpu_line)[0])
        elif platform.system() == 'Darwin':  # macOS
            # macOS 使用 top -l 1 -n 0
            result = subprocess.run(['top', '-l', '1', '-n', '0'], stdout=subprocess.PIPE, text=True)
            output = result.stdout
            cpu_line = [line for line in output.split('\n') if 'CPU usage' in line][0]
            cpu_usage = 100 - float(re.findall(r'(\d+\.\d+)% idle', cpu_line)[0])
        else:
            # 其他系统使用 psutil
            cpu_usage = psutil.cpu_percent()

        # 获取负载平均值
        load_avg = [float(x) for x in psutil.getloadavg()]

        return {
            'cpu_usage': round(cpu_usage, 2),
            'cpu_load_1': load_avg[0],
            'cpu_load_5': load_avg[1],
            'cpu_load_15': load_avg[2]
        }
    except Exception as e:
        print(f"Error getting CPU info: {e}")
        # 如果命令不可用，使用psutil作为备选
        return {
            'cpu_usage': round(psutil.cpu_percent(), 2),
            'cpu_load_1': psutil.getloadavg()[0],
            'cpu_load_5': psutil.getloadavg()[1],
            'cpu_load_15': psutil.getloadavg()[2]
        }


def get_memory_info():
    """获取内存信息"""
    mem = psutil.virtual_memory()
    return {
        'mem_total': mem.total,
        'mem_used': mem.used,
        'mem_free': mem.free,
        'mem_usage': round(mem.percent, 2)
    }


def get_disk_info():
    """获取磁盘信息"""
    disk = psutil.disk_usage('/')
    return {
        'disk_total': disk.total,
        'disk_used': disk.used,
        'disk_free': disk.free,
        'disk_usage': round(disk.percent, 2)
    }


def get_network_info():
    """获取网络信息"""
    net_io = psutil.net_io_counters()
    return {
        'net_sent': net_io.bytes_sent,
        'net_recv': net_io.bytes_recv
    }


def collect_system_metrics():
    """收集所有系统指标"""
    metrics = {}
    metrics.update(get_cpu_info())
    metrics.update(get_memory_info())
    metrics.update(get_disk_info())
    metrics.update(get_network_info())
    return metrics
