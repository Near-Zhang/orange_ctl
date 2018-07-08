from django.db.models import Model
from django.db.models import CharField,IntegerField

class Nodes(Model):
    ip = CharField(max_length=16)
    location = CharField(max_length=32)
    enable = IntegerField()


