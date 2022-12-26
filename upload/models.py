from django.db import models

class Upload(models.Model):
    file =models.FileField(upload_to='uploadfiles/',null=True)
    file_name =models.CharField(max_length=100)
    file_path =models.CharField(max_length=200)

    def __str__(self):
        return self.file
