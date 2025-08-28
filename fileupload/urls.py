from django.urls import path

from board.views import boardDetail
from .views import *

urlpatterns=[
    path('<int:pk>/', boardDetail,name='image'),
]