from django.shortcuts import get_object_or_404, redirect
from rest_framework import generics, status
from rest_framework.response import Response
from .models import ShortenedURL
from .serializers import ShortenedURLSerializer

class ShortenedURLCreateView(generics.CreateAPIView):
    """
    API view para criar URLs encurtadas.
    """
    queryset = ShortenedURL.objects.all()
    serializer_class = ShortenedURLSerializer

def redirect_view(request, short_code):
    """
    View que recebe o código curto e redireciona para a URL original.
    """
    shortened_url = get_object_or_404(ShortenedURL, short_code=short_code)
    return redirect(shortened_url.original_url)
