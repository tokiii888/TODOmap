from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.http import HttpResponse

class SignUp(CreateView):
  template_name = 'registration/signup.html'
  form_class = UserCreationForm
  success_url = reverse_lazy('login')

def index(request):
  return HttpResponse("You're voting on question")
