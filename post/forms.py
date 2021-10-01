from django import forms
from .models import Post, Comment

class Add_EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)


class Add_Commen_Add_Reply_Form(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)