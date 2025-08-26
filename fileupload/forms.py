from django.forms import ModelForm, forms

from fileupload.models import FileUpload


class FileUploadForm(ModelForm):
    class Meta:
        model = FileUpload
        fields=['title','imgfile','content']