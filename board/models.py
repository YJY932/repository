from tkinter.constants import CASCADE

from django.utils import timezone

from django.contrib.auth.models import User
from django.db import models

import board


# Create your models here.

class Board(models.Model):
    # Board 모델 : models.Model을 상속받아 정의됨. models.Model은 장고에서 제공하는 모델의 기본 클래스로 데이터베이스 모델을 정의할 때 사용됨. 장고의 ORM(Object-Relational Mapping)을 사용하여 데이터베이스와 상호작용 할 수 있음. 모델을 정의한 이후에는 장고의 migration 기능을 사용하여 데이터베이스 스키마를 업데이느 할 수 있음
    # Board 모델의 필드 세개
    title=models.CharField(max_length=20,null=True)
    content=models.TextField()
    # writer=models.CharField(max_length=20,null=True)
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True)
    date=models.DateTimeField(default=timezone.now)
    # user : User 모델과의 관계를 나타내는 외래키 필드. 게시글 작성한 사용자를 저장
    # User 모델 : 장고에서 제공하는 기본 모델 중 하나, 사용자 정보를 저장.
    # on_delete=models.DO_NOTHING : 참조하는 객체(User)가 삭제되었을 때 아무 동작도 하지 않겠다. null=True : 이 필드는 비어있을 수 있음

    def __str__(self):
        return self.title

class Image(models.Model):
    board_image=models.ForeignKey(Board,on_delete=models.CASCADE,related_name='images',null=True)
    image=models.ImageField(upload_to='board/%Y/%m/%d',null=True,blank=True)

class Comments(models.Model):
    board_comment=models.ForeignKey(Board,related_name='comments',on_delete=models.CASCADE)
    # related_name='comments' : post.comments.all()을 통해 comments에 접근할 수 있음
    content_comment=models.TextField() # 댓글 입력 필드
    user_comment=models.ForeignKey(User,on_delete=models.CASCADE)
    date_comment=models.DateTimeField(default=timezone.now) # default=timezone.now로 설정되어 있으므로 저장할 때 자동으로 들어감. 사용자가 입력하지도 뷰에서 따로 설정하지도 않음.

    def __str__(self):
        return f'Comment by {self.user_comment.username} on {self.board_comment.title}'