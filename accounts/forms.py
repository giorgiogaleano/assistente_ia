from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
# from django.http import HttpResponse
from django.db.models import Q

class CustomUserCreationForm(UserCreationForm): 
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })

        self.fields['username'].widget.attrs.update({'placeholder': 'Inserisci il nome utente'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Inserisci un indirizzo email valido'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Crea una password sicura'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Conferma la password'})

# accesso tramite email o nome utente
class EmailOrUsernameAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username o email', required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # oltre alle solite funzioni di clean(), controlla se il valore inserito è un username o una email e verifica se l'utente esiste nel db
    def clean(self):
        cleaned_data = self.cleaned_data  # Si leggono i dati già puliti dai singoli campi senza invocare super().clean()
        identifier = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if identifier and password:
            user = User.objects.filter(
                Q(username=identifier) | Q(email=identifier) # confronta l'identifier sia all'username che alla mail nella stessa query
            ).first() # si usa first() invece di get() perché se l'utente non esiste first lo imposta uguale a None, mentre get crasha con l'errore DoesNotExist

            if user:
                self.user_cache = authenticate(
                    self.request,
                    username=user.username,
                    password=password
                )
            
            # fuori da 'if user:' per catturare anche il caso in cui l'utente non venga trovato
            if self.user_cache is None:
                raise forms.ValidationError("Credenziali non valide. Riprova.")

        return cleaned_data

        



''' questa sessione sarà dedicata al recupero della password '''

# form che chiede la mail quando clicchi su "password dimenticata"
class RequestPasswordResetForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Inserisci la tua email'}),
        required=True
    )
# verifica che il codice inserito sia corretto
class ResetPasswordConfirmForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Codice a 6 cifre'}),
        required=True
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nuova password'}),
        required=True
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Conferma nuova password'}),
        required=True
    )

    def clean(self):
        self.cleaned_data=super().clean()
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2: #se (1) esistono p1 e p2 e (2) non sono uguali
            raise forms.ValidationError("Le due password non coincidono.")
        return self.cleaned_data