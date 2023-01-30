import datetime,uuid
from django.db import models

class Database(models.Model):
    id=models.IntegerField(primary_key=True,auto_created=True,default=1)
    database_name=models.CharField(max_length=100,blank=True,unique=True,null=True)

    def __str__(self):
        return self.database_name

class Project(models.Model):
    id=models.IntegerField(primary_key=True,auto_created=True,default=1)
    project_name=models.CharField(max_length=100,blank=True,unique=True,null=True)
    user_name=models.CharField(max_length=100,blank=True,null=True)
    description=models.CharField(max_length=100,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def __str__(self):
        return self.project_name

class DataSource(models.Model):
    project_id=models.BigIntegerField()
    data_source=models.CharField(max_length=100,blank=True,null=True)
    table_records=models.IntegerField(blank=True,null=True)
    total_records=models.IntegerField(blank=True,null=True)
    final_data_file_generate=models.CharField(max_length=200,blank = True,null=True)
    created_at=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at=models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def __str__(self):
        return self.data_source


class Upload(models.Model):
    project_name=models.CharField(max_length=100,default=None,null=True)
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
    updated_at=models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.file

class DataQualityCheck(models.Model):
    id =models.IntegerField(primary_key=True,auto_created=True)
    data_source=models.CharField(max_length=200,blank = True,null=True)
    column_name=models.CharField(max_length=200,blank = True,null=True)
    null_check=models.BooleanField(default=False,blank= True,null=True)
    date_check=models.BooleanField(default=False,blank= True,null=True)
    special_character_check=models.BooleanField(default=False,blank= True,null=True)
    string_check=models.BooleanField(default=False,blank= True,null=True)
    integer_check=models.BooleanField(default=False,blank= True,null=True)
    created_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.column_name

class Transformation(models.Model):
    id =models.IntegerField(primary_key=True,auto_created=True)
    data_source=models.CharField(max_length=200,blank = True,null=True)
    column_name=models.CharField(max_length=200,blank = True,null=True)
    date_transformation=models.BooleanField(default=False,blank= True,null=True)
    currency_transformation=models.BooleanField(default=False,blank= True,null=True)
    roundoff_transformation=models.BooleanField(default=False,blank= True,null=True)
    created_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.column_name

class QueryLogs(models.Model):
    id =models.IntegerField(primary_key=True,auto_created=True)
    project_id=models.IntegerField(blank = True,null=True)
    data_source=models.IntegerField(blank = True,null=True)
    query_statement=models.CharField(max_length=1000,blank = True,null=True)
    target_table=models.CharField(max_length=100,blank = True,null=True)
    created_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.query_statement