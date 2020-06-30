import django.contrib.admin.helpers as helpers
from django import forms
from project.apps.curiosity.models import PostComment



class PostCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = "__all__"