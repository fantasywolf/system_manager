import psutil


def get_cpu_info():
    """获取CPU信息"""

    cpu_usage = psutil.cpu_percent(interval=1)

    # 获取负载平均值
    load_avg = [float(x) for x in psutil.getloadavg()]

    return {
        'cpu_usage': round(cpu_usage, 2),
        'cpu_load_1': load_avg[0],
        'cpu_load_5': load_avg[1],
        'cpu_load_15': load_avg[2]
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

if __name__ == '__main__':
    print(collect_system_metrics())