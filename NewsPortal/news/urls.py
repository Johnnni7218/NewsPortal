from django.urls import path
from .views import AuthorList, CategoryListView, subscribe
from .views import PostsList, PostDetail, PostCreate, NewsCreate, PostUpdate, NewsUpdate, PostDelete, NewsDelete
from .views import CategoryList
from .views import CommentList
from .views import upgrade_me


urlpatterns = [
   path('', PostsList.as_view(), name='post_list'),
   path('author/', AuthorList.as_view()),
   path('category/', CategoryList.as_view()),
   path('comment/', CommentList.as_view()),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('post/create/', PostCreate.as_view(), name='post_create'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('post/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('news/<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
   path('post/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('upgrade/', upgrade_me, name='upgrade'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
]
