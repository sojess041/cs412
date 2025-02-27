from django.urls import path
from .views import * #ShowAllView, ArticleView, RandomArticleView

urlpatterns = [
    path('', ShowAllView.as_view(), name="show_all"),
    path('article/<int:pk>/', ArticleView.as_view(), name="article"),
    path('random/', RandomArticleView.as_view(), name="random_article"),
    path('article/create/', CreateArticleView.as_view(), name="create_article"),
    path('article/<int:pk>/create_comment', CreateCommentView.as_view(), name = "create_comment"), 
    


]

