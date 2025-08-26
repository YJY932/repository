from django.db import models

# Create your models here.
class FileUpload(models.Model):
    title = models.CharField(max_length=100,null=True)
    imgfile=models.ImageField(upload_to='',blank=True) # upload_to='' : MEDIA_ROOT
    content = models.TextField()

    def __str__(self):
        return self.title