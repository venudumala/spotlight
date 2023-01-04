import datetime,uuid
from django.db import models

class Upload(models.Model):
    record_id=models.UUIDField(default=uuid.uuid4,editable = False,unique=True,max_length=100,null=True)
    file =models.FileField(upload_to='uploadfiles/',default=None)
    file_name =models.CharField(max_length=100,default=None,null=True)
    file_type =models.CharField(max_length=200,blank = True,null=True)
    upoload_layer=models.BooleanField(default=False,blank = True,null=True)
    dump_layer=models.BooleanField(default=False,blank= True,null=True)
    transformation_layer=models.BooleanField(default=False,blank=True,null=True)
    records_inserted=models.BigIntegerField(blank = True,null=True)
    valid_file_path=models.CharField(max_length=200,blank = True,null=True)
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(null=True)

    def __str__(self):
        return self.file