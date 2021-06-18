from django.shortcuts import render
# from .models import User
# Create your views here.
def index(request):
    # num_users = User.objects.all().count()
    num_users = 10
    return render(
        request,
        'index.html',
        context={'num_users': num_users},
    )