from django.shortcuts import render, redirect

# from .models import User
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('teachers:competition_list')
        else:
            return redirect('students:competition_list')

    return render(request, 'start_page.html')

def to_competition(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('teachers:competition_list')
        else:
            return redirect('students:competition_list')

    return redirect( '/accounts/login/')



