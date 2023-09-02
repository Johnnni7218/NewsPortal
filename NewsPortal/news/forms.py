from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class PostForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = [
           'name_post',
           'body_post',
           'author',
           'category'
       ]

   def clean(self):
       cleaned_data = super().clean()
       body_post = cleaned_data.get("body_post")
       if body_post is not None and len(body_post) < 30:
           raise ValidationError({
               "body_post": "Текст не может быть менее 30 символов."
           })
       name_post = cleaned_data.get("name_post")
       if name_post == body_post:
           raise ValidationError(
               "Текст не должен быть идентичен названию."
           )
       return cleaned_data
