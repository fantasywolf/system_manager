# models.py
from django.db import models
from django.utils import timezone


class Test(models.Model):
    name = models.CharField(max_length=20)

class SystemMetrics(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)

    # CPU 信息
    cpu_usage = models.CharField(max_length=100,help_text="CPU使用率(%)")
    cpu_load_1 = models.FloatField(help_text="1分钟平均负载")
    cpu_load_5 = models.FloatField(help_text="5分钟平均负载")
    cpu_load_15 = models.FloatField(help_text="15分钟平均负载")

    # 内存信息
    mem_total = models.BigIntegerField(help_text="总内存(字节)")
    mem_used = models.BigIntegerField(help_text="已用内存(字节)")
    mem_free = models.BigIntegerField(help_text="空闲内存(字节)")
    mem_usage = models.FloatField(help_text="内存使用率(%)")

    # 磁盘信息
    disk_total = models.BigIntegerField(help_text="总磁盘空间(字节)")
    disk_used = models.BigIntegerField(help_text="已用磁盘空间(字节)")
    disk_free = models.BigIntegerField(help_text="空闲磁盘空间(字节)")
    disk_usage = models.FloatField(help_text="磁盘使用率(%)")

    # 网络信息
    net_sent = models.BigIntegerField(help_text="发送字节数")
    net_recv = models.BigIntegerField(help_text="接收字节数")
