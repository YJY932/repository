from django.urls import path
from .views import *

urlpatterns=[
    path('', fileupload,name='fileupload'),
]