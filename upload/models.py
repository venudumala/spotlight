import datetime,uuid
from django.db import models

class Upload(models.Model):
    record_id=models.UUIDField(default=uuid.uuid4,editable = False,unique=True,max_length=100,null=True)
    file =models.FileField(upload_to='uploadfiles/',null=True)
    file_name =models.CharField(max_length=100)
    file_type =models.CharField(max_length=200)
    upoload_layer=models.BooleanField(default=False,null=True)
    dump_layer=models.BooleanField(default=False,null=True)
    transformation_layer=models.BooleanField(default=False,null=True)
    records_inserted=models.BigIntegerField(default=0,null=True)
    created_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file