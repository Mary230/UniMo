from django.shortcuts import redirect, render
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from catalog.forms import DownCompFileForm # новый
from catalog.models import CompetitionFile

class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


# def index(request):
#     # num_users = User.objects.all().count()
#     num_users = 10
#     return render(
#         request,
#         'start_page.html',
#         context={'num_users': num_users},
#     )

class CreatePostView(CreateView): # новый
    model = CompetitionFile
    form_class = DownCompFileForm
    template_name = 'post.html'
    success_url = reverse_lazy('home')