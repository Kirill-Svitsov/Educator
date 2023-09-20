from django import forms
from .models import Comment, Task


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'code', 'category', 'subject']
