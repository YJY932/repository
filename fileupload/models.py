from django.db import models

from board.models import Board


# Create your models here.
class FileUpload(models.Model):
    board_image=models.ForeignKey(Board,on_delete=models.CASCADE,related_name='uploaded_images',null=True,blank=True)
    # title = models.CharField(max_length=100,null=True)
    imgfile=models.ImageField(upload_to='board/%Y/%m/%d',blank=True) # upload_to='' : MEDIA_ROOT, upload_to='board/%Y/%m/%d' : 날짜별로 폴더가 생김
    # content = models.TextField(blank=True,null=True)

    def __str__(self):
        return f"Image for: {self.board_image.title if self.board_image else 'No Board'}"
    # 제목이 있다 -> Image for: 제목/제목이 없더 -> Image for: No Board