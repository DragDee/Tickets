from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
import random, string

from .models import Flyes, SoldTickets

class AddFlyghtForm(forms.ModelForm):
    class Meta:
        model = Flyes
        fields = '__all__'


class SearchFlyForm(forms.Form):
    arrival = forms.CharField(required=False, max_length=100, label='Город вылет')
    departure = forms.CharField(required=False, max_length=100, label='Пункт прибытия')
    arrival_date = forms.DateField(required=False, label='Время и дата вылета')
    departure_date = forms.DateField(required=False, label='Время и дата прибытия')
    price1 = forms.FloatField(required=False, label='Мин цена')
    price2 = forms.FloatField(required=False, label='Макс цена')

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form'}))
    last_name = forms.CharField(label='Фамилию', widget=forms.TextInput(attrs={'class': 'form'}))
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name')

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form'}))

class ChangeBalanceForm(forms.Form):
    balance = forms.FloatField(label='Ваш баланс', required=False)

class UserForCashierForm(forms.Form):
    name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form'}))
    surname = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form'}))

    def get_random_str(self, length=10):
        characters = string.ascii_letters + string.digits  # Все буквы и цифры
        random_string = ''.join(random.choice(characters) for i in range(length))
        return random_string


