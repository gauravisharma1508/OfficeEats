"""
from django import forms
from .models import Image

class ImageForm(forms.ModelForm):
    class Meta:
        model=Image
        fields=( 'fname','oname','emp_id', 'mob', 'email','image')

 """       