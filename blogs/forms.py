from django.forms import fields
from .models import CommentModel, PostModel,Category
from django import forms

class PostForm(forms.ModelForm):

    class Meta:
        model=PostModel
        fields=["title","description","image", "is_published","categories"]
        categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,)


class CommentForm(forms.ModelForm):

    class Meta:
        model=CommentModel
        fields=["comment","post","commenter"]


