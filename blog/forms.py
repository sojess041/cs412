from django import forms
from .models import Article, Comment

class CreateArticleForm(forms.ModelForm):
    "form to add an article to the database"

    class Meta: 
        "associate this form with a model from database"
        model = Article
        fields = ['author', 'title', 'text', 'image_url']
class CreateCommentForm(forms.ModelForm):
    "associate this form with a model from our database."
    model = Comment 
    fields = ['author', 'text']
