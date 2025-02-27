from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView 
from .models import Article
from .forms import CreateArticleForm, CreateCommentForm
from django.urls import reverse 

import random
# Create your views here.

class ShowAllView(ListView):
    '''Define view class to show all blog articles'''

    model = Article 
    template_name = "blog/show_all.html"
    context_object_name = "articles"



class ArticleView(DetailView):
    model = Article 
    template_name = "blog/article.html"
    context_object_name = "article"


class RandomArticleView(DetailView):
    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"

    def get_object(self):
        all_articles = Article.objects.all()
        return random.choice(all_articles)
    
class CreateArticleView(CreateView):
    "A view to handle creation of a new article"
    "1. display html form to user(GET)"
    "2. process the form submission and store the new article object(POST)"

    form_class = CreateArticleForm

    template_name = "blog/create_article_form.html"


class CreateCommentView(CreateView):
    "a view to handle the craetion of a new comment on an article"
    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    def get_success_url(self):
        "provide url to redirect to after creating a comment"
        #return reverse('show_all')
        pk = self.kwargs['pk']
        return reverse('article', kwargs={'pk':pk})
    
    def get_context_data(self):
        "return the dictionary of context variables for use in the template"
        #calling the superclass method
        context = super().get_context_data

        #find/add the article to the context data 
        #retrieve the PK from the URL pattern 
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)

        #add this article into the context dictionary
        context['article'] = article
        return context 
    
    def form_valid(self, form):
        "handles the form submission and saves the new object to the django database"

        "need to add foreign key"

        print(form.cleaned_data)
        pk = self.kwargs['pk']
        article = Article.objects.get(pk = pk)
        #attach this article to the comment
        form.instance.article = article #set the FK 


        #delegate work to the superclass method form_valid:
        return super().form_valid(form)
    





