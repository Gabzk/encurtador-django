from django.urls import path
from .views import ShortenedURLCreateView

urlpatterns = [
    path('urls/', ShortenedURLCreateView.as_view(), name='url-create'),
]
