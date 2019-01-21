from django.db import models


class Nodes(models.Model):

    class Meta:
        verbose_name = '节点'
        db_table = 'nodes'
        unique_together = ('ip', 'port')

    ip = models.CharField(max_length=16, verbose_name='IP')
    port = models.CharField(max_length=8, verbose_name='端口')
    location = models.CharField(max_length=32, verbose_name='地区')
    enable = models.BooleanField(default=True, verbose_name='是否启用')
    master = models.BooleanField(default=False, verbose_name='是否主节点')

    def serialize(self):
        """
        对象序列化
        :return: dict
        """
        d = self.__dict__.copy()
        del d['_state']
        return d

