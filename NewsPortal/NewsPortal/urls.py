from django.contrib import admin
from django.urls import path, include
from news.views import EntranceList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('posts/', include('news.urls')),
    path('accounts/', include('allauth.urls')),
    path('', EntranceList.as_view()),
]
