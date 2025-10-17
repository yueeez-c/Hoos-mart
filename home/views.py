from django.shortcuts import render
from django.http import HttpResponse
from .models import Post

def home (request):
	context = {
		'posts' : Post.objects.all()
	}
	return render(request, 'home/home.html')

def about (request):
	return render(request, 'home/about.html')


# Create your views here.
