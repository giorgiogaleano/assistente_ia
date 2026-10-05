from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from .forms import CustomUserCreationForm, RequestPasswordResetForm, ResetPasswordConfirmForm
import random # per generare il numero casuale per il recupero della password
from django.core.mail import send_mail
from django.contrib.auth.models import User


def register(request):
    # se l'utente è loggato lo porta automaticamente a una nuova chat
    # if request.user.is_authenticated:
    #     return redirect('chat:new_chat')
    # altrimenti, se ha compilato il form
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) #logga l'utente in automatico dopo la registrazione
            return redirect('chat:new_chat')
    # se il form è vuoto o non è stato compilato correttamente
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form':form})

def password_reset_request(request):
    if request.method == 'POST':
        form = RequestPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                code = str(random.randint(100000, 999999)) # genera il codice monouso

                # salva il codice e l'id dell'utente nella sessione del browser
                request.session['reset_code'] = code
                request.session['reset_user_id'] = user.pk

                # simula l'invio della mail stampandola sulla console
                send_mail(
                    'Codice di recupero password',
                    f'Il tuo codice monouso è {code}',
                    'email@email.com',
                    [email],
                    fail_silently=False
                )
            return redirect('accounts:password_reset_confirm')
    else:
        form = RequestPasswordResetForm()

    return render(request, 'accounts/password_reset_request.html', {'form' : form})

def password_reset_confirm(request):
    # se l'utente non ha richiesto un codice lo reindirizza al primo passaggio (controlla se nella sessione c'è la variabile 'reset_code')
    if 'reset_code' not in request.session:
        return redirect('accounts:password_reset_request')

    # invece, se ha richiesto un codice
    if request.method == 'POST':
        form = ResetPasswordConfirmForm(request.POST)
        if form.is_valid():
            input_code = form.cleaned_data['code'] # codice inserito dall'utente
            session_code = request.session.get('reset_code') # dalla sessione, prende il codice generato automaticamente

            if input_code == session_code:
                user_id = request.session.get('reset_user_id')
                user = User.objects.get(pk=user_id)

                # cripta e salva la nuova password
                user.set_password(form.cleaned_data['password1'])
                user.save()

                # elimina i dati temporanei della sessione
                del request.session['reset_code']
                del request.session['reset_user_id']

                return redirect('accounts:login')
            else:
                form.add_error('code', 'Il codice inserito non è corretto')
    else:
        form = ResetPasswordConfirmForm()

    return render(request, 'accounts/password_reset_confirm.html', {'form':form})
