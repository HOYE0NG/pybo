from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm
from pybo.models import Question, Answer, Comment

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password) # 사용자 인증
            login(request, user)
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})

def find_password(request):
    return render(request, 'common/find_password.html')

def state(request):
    question_list = Question.objects.filter(author__username=request.user)
    context = {
        'question_list':question_list,
    }
    return render(request, 'common/state.html', context)