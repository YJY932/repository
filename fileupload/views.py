from django.shortcuts import render, redirect
from matplotlib.pyplot import title

from .forms import FileUploadForm
from .models import FileUpload

# Create your views here.
def fileupload(request):
    if request.method=='POST':
        title=request.POST['title']
        content=request.POST['content']
        img=request.FILES['imgfile']
        fileupload=FileUpload(title=title,
                              imgfile=img,
                              content=content,
                              )
        fileupload.save()
        return redirect('fileupload')
    else:
        fileuploadForm=FileUploadForm
        context={
            'fileuploadForm':fileuploadForm,
        }
        return render(request,'fileupload/fileupload.html',context)