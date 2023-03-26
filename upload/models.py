import datetime,uuid
from django.db import models
from django.contrib.auth.models import User 

class Database(models.Model):
    id=models.IntegerField(primary_key=True,auto_created=True,default=1)
    database_name=models.CharField(max_length=100,blank=True,unique=True,null=True)

    def __str__(self):
        return self.database_name

class Project(models.Model):
    project_name=models.CharField(max_length=100,blank=True,unique=True,null=True)
    user_id=models.IntegerField()
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
    data_source=models.CharField(max_length=200,blank = True,null=True)
    column_name=models.CharField(max_length=200,blank = True,null=True)
    null_check=models.BooleanField(default=False,blank= True,null=True)
    date_check=models.BooleanField(default=False,blank= True,null=True)
    special_character_check=models.BooleanField(default=False,blank= True,null=True)
    string_check=models.BooleanField(default=False,blank= True,null=True)
    integer_check=models.BooleanField(default=False,blank= True,null=True)
    created_at=models.DateTimeField(auto_now=True,blank= True,null=True)

    def __str__(self):
        return self.column_name

class Transformation(models.Model):
    data_source=models.CharField(max_length=200,blank = True,null=True)
    column_name=models.CharField(max_length=200,blank = True,null=True)
    date_transformation=models.BooleanField(default=False,blank= True,null=True)
    currency_transformation=models.BooleanField(default=False,blank= True,null=True)
    roundoff_transformation=models.BooleanField(default=False,blank= True,null=True)
    created_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.column_name

class QueryLogs(models.Model):
    project_id=models.IntegerField(blank = True,null=True)
    data_source=models.IntegerField(blank = True,null=True)
    query_statement=models.CharField(max_length=1000,blank = True,null=True)
    target_table=models.CharField(max_length=100,blank = True,null=True)
    created_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.query_statement

class DataType(models.Model):
    datatype=models.CharField(max_length=1000,blank = True,null=True)
    created_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.DataType

class filterSymbol(models.Model):
    symbol=models.CharField(max_length=10,blank = True,null=True)
    created_at=models.DateTimeField(auto_now=True,blank= True,null=True)

class goldLayerData(models.Model):
    project_name=models.CharField(max_length=1000,blank = True,null=True)
    data_source=models.CharField(max_length=1000,blank = True,null=True)
    records_inserted=models.CharField(max_length=1000,blank = True,null=True)
    final_data_file_generate=models.CharField(max_length=1000,blank = True,null=True)

class workflowRules(models.Model):
    project_id = models.IntegerField(blank=True,null=True)
    layer = models.CharField(max_length=100,blank = True,null=True)
    created_by = models.CharField(max_length=100,blank = True,null=True)
    created_at = models.DateTimeField(auto_now=True,blank = True,null=True)
    description = models.CharField(max_length=1000,blank = True,null=True)
    rule_name = models.CharField(max_length=1000,blank = True,null=True)
    is_active = models.BooleanField(blank=True,null=True)
    source_table = models.CharField(max_length=1000,blank = True,null=True)
    target_table = models.CharField(max_length=1000,blank = True,null=True)
    rules_data = models.TextField(blank=True,null=True)


    def __str__(self):
        return self.rule_name

    
class layerDetails(models.Model):
    layerName= models.CharField(max_length=100,blank = True,null=True)
    created_at=models.DateTimeField(auto_now=True,blank= True,null=True)

    def __str__(self):
        return self.layerName
    
class workflowTransition(models.Model):
    projectId = models.ForeignKey(Project,on_delete=models.CASCADE,related_name="workflowRules")
    layerId = models.ForeignKey(layerDetails,on_delete=models.CASCADE,related_name="workflowRules")
    ruleId= models.ForeignKey(workflowRules,on_delete=models.CASCADE,related_name="workflowRules")
    isActive = models.BooleanField(blank=True,null=True)
    created_by = models.CharField(max_length=100,blank = True,null=True)
    created_at = models.DateTimeField(auto_now=True,blank = True,null=True)


class Audit(models.Model):
  UID=models.UUIDField(primary_key=True,auto_created=True,default=uuid.uuid4,editable=False)
  PROJECT_ID=models.IntegerField(default=None)
  DATASOURCE=models.CharField(max_length=500,default=None)
  OPERATION=models.CharField(max_length=20,default=None)
  CREATED_BY=models.CharField(max_length=100,null=True)
  CREATED_AT=models.DateTimeField(auto_now_add=True,null=True)
  CALLED_FUNCTION_NAME=models.CharField(max_length=200,null=True)
  LAYER=models.CharField(max_length=200,default=None,null=True)
  TABLE_NAME=models.CharField(max_length=200,default=None,null=True)
  STATUS=models.CharField(max_length=10,default=None,null=True)
  MESSAGE=models.CharField(max_length=500,default=None,null=True)
  def __str__(self):
    return self.OPERATION