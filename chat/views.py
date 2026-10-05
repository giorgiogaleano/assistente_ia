from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required

def new_chat(request):
        return render(request, 'chat/new_chat.html')