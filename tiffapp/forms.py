from django import forms

class FolderInputForm(forms.Form):
    folders = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}), label='Folders (comma-separated)')
    output_file = forms.CharField(max_length=100, label='Output TIFF file name')
