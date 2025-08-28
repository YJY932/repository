from django.forms import ModelForm, forms

from fileupload.models import FileUpload


class FileUploadForm(ModelForm):
    class Meta:
        model = FileUpload
        fields=['imgfile'] # 이미지 필드만 처리