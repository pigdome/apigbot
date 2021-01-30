from django.db import models
from django.utils import timezone

class LineUser(models.Model):
    objects     = models.Manager()
    id          = models.AutoField(primary_key=True)
    line_name   = models.CharField(max_length=60)
    line_id     = models.CharField(max_length=60)
    verify      = models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)   
    
    def __str__(self):
        return super().__str__()