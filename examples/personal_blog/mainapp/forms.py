from django import forms

from mainapp.models import PostItem


class PostCreationForm(forms.ModelForm):
    class Meta:
        model = PostItem
        exclude = ('blog', 'created', )
