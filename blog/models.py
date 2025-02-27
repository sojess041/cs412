#blog/models.py 
from django.db import models
from django.urls import reverse



# Create your models here.
class Article(models.Model):
    '''Encapsulate the data of a blog Article by an author'''

    #define the data attributes of this Article object
    title = models.TextField(blank=True)
    author = models.TextField(blank=True)
    text = models.TextField(blank=True)
    published = models.DateTimeField(auto_now = True)
    image_url = models.URLField(blank = True)




    def __str__(self):
        '''return a format string'''
        return f'{self.title} by {self.author}'
    

    def get_absolute_url(self):
        "return url to display one instance of the object"
        return reverse('article', kwargs={'pk':self.pk})
    
    def get_all_comments(self):
        "return a queryset of comments about this article"

        comments = Comment.objects.filter(article=self)

class Comment(models.Model):
    'encapsultate the idea of a comment about an article'
    article = models.ForeignKey(Article, on_delete = models.CASCADE)

    author = models.TextField(blank = False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now = True)

    def __str__(self):
        "return a string rep of thsi comment"
        return f'{self.text}'
    

    