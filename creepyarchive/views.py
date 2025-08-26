from django.shortcuts import render

from board.forms import BoardForm


def home(request):
    form=BoardForm()
    return render(request, 'board.html',{'boardForm':form})