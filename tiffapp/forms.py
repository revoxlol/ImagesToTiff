from django import forms
from multiupload.fields import MultiFileField

class ImageUploadForm(forms.Form):
    images = MultiFileField(min_num=1, max_num=10, max_file_size=1024*1024*5, required=True, label='Select images')
    output_file = forms.CharField(max_length=100, label='Output TIFF file name')