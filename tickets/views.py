from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import Flyes, SoldTickets, UserProfile
from django.contrib.auth.models import User
from .forms import SearchFlyForm, AddFlyghtForm, RegisterUserForm, LoginUserForm, ChangeBalanceForm, UserCreationForm, \
    UserForCashierForm
from datetime import date


# Create your views here.

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = "tickets/registration.html"
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Регистрация"
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        profile = UserProfile(user=user, balance=0)
        profile.save()
        return redirect('home')

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "tickets/login.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Логин"
        return context

    def get_success_url(self):
        return reverse_lazy('home')

class FlyesView(ListView):
    model = Flyes
    template_name = "tickets/allFlyes.html"
    context_object_name = "tickets"
    allow_empty = False#можно лит чтоб набор был пуст

    def get_context_data(self, *, objectlist=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Список всех рейсов"
        return context

    def get_queryset(self):
        #id_num = self.kwargs['flightid']
        return Flyes.objects.filter(pk__gte=0)


class SoldTicketsView(ListView):
    model = SoldTickets
    template_name = "tickets/soldTickets.html"
    context_object_name = "tickets"

    def get_context_data(self, *, objectlist=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Список проданых билетов"
        return context

class FlightView(DetailView):
    model = Flyes
    template_name = "tickets/flight.html"
    context_object_name = "flight"
    #slug_url_kwarg = "flightid"
    pk_url_kwarg = "flightid"

    def get_context_data(self, *, objectlist=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Информация о билете"
        return context

def index(request):
    tickets = Flyes.objects.all()
    context = {
        "content": "This is ciontent",
        "tickets": tickets
    }
    return render(request, "tickets/index.html", context)

def soldTickets(request):
    tickets = SoldTickets.objects.all()

    if not request.user.is_staff:
        return redirect('home')

    context = {
        "title": "Список всех проданных билетов",
        "header": "Список всех проданных билетов",
        "tickets": tickets
    }
    return render(request, "tickets/soldTickets.html", context)

def allFlyes(request):
    tickets = Flyes.objects.all()
    context = {
        "content": "This is ciontent",
        "header": "Список всех рейсов",
        "tickets": tickets
    }
    return render(request, "tickets/allFlyes.html", context)

def info(request):
    return render(request, "tickets/info.html", {
        "content" : "This is content",
    })

def flyght_search(request):
    kw = {}
    search_results = Flyes.objects.all()

    if request.method == 'POST':
        form = SearchFlyForm(request.POST)
        if form.is_valid():
            for i in form.cleaned_data:
                if request.POST[i] and i != 'price1' and i != 'price2':
                    kw[i] = request.POST[i]
            print(kw)
            search_results = search_results.filter(**kw)

            if form.cleaned_data['price1']:
                search_results = search_results.filter(price__gte=form.cleaned_data['price1'])

            if form.cleaned_data['price2']:
                search_results = search_results.filter(price__lte=form.cleaned_data['price2'])

            for i in search_results:
                print(i)
    else:
        form = SearchFlyForm()

    context = {
        "title": "Рейс",
        "flight": flight,
        "form": form,
        "search_results": search_results
    }
    return render(request, "tickets/search_flyght.html", context)

def flight(request, flightid):
    flight = Flyes.objects.get(pk=flightid)
    context = {
        "title": "Рейс",
        "flight": flight
    }
    return render(request, "tickets/flight.html", context)

def buy_tickets(request, flight_id):
    if request.user.is_staff:
        return buy_as_cashier(request, flight_id)

    flight0 = Flyes.objects.get(id=flight_id)
    profile = get_object_or_404(UserProfile, user=request.user)
    context = {
        "title": "Рейс",
    }


    if flight0.price <= profile.balance and flight0.quantity > 0:

        try:
            last_place = SoldTickets.objects.filter(flyes_id_id=flight_id).order_by('-place_number')[0].place_number
        except:
            last_place = 0

        b = SoldTickets(flyes_id=flight0, user=request.user, place_number=last_place+1)
        b.save()

        flight0.quantity -= 1
        flight0.save()
        profile.bought_tickets.add(b)
        profile.balance -= flight0.price
        profile.save()



        context["message"] = "Билет успешно приобретён"

    else:
        context["message"] = "На счету пользователя не хватает средст"

    return render(request, "tickets/index.html", context)

def buy_as_cashier(request, flight_id):
    context = {
        "title": "buy_as_cashier",
    }

    if request.user.is_staff:
        form = UserForCashierForm(request.POST)
        context['form'] = form
        if form.is_valid():
            first_name = request.POST['name']
            last_name = request.POST['surname']
            username = form.get_random_str()
            password = form.get_random_str()
            custom_user = User(first_name=first_name, last_name=last_name, username=username)
            custom_user.set_password(password)
            custom_user.save()
            print(username)
            print(password)

            profile = UserProfile(user=custom_user)
            profile.save()

            flight0 = get_object_or_404(Flyes, id=flight_id)

            if flight0.quantity > 0:
                try:
                    last_place = SoldTickets.objects.filter(flyes_id_id=flight_id).order_by('-place_number')[
                        0].place_number
                except:
                    last_place = 0

                b = SoldTickets(flyes_id=flight0, user=custom_user, place_number=last_place + 1, cashier=request.user.id)
                b.save()

                flight0.quantity -= 1
                flight0.save()
                profile.bought_tickets.add(b)
                profile.balance -= flight0.price
                profile.save()

                context['message'] = "Покупка произведенна успешно"
                context['success'] = True
                context['username'] = username
                context['password'] = password


    return render(request, "tickets/buy_as_cashier.html", context)

def refund(request, ticket_id):
    soldticket = get_object_or_404(SoldTickets, id=ticket_id)
    flight0 = soldticket.flyes_id
    ticket_price = soldticket.flyes_id.price
    profile = get_object_or_404(UserProfile, user=soldticket.user)
    context = {
        "title": "Рейс",
    }

    try:
        soldticket.delete()
        profile.balance += ticket_price
        flight0.quantity += 1
        flight0.save()
        profile.save()
        context["message"] = "Удаление произошло успешно"

    except:
        context["message"] = "При удалении возникла ошибка"

    return render(request, "tickets/index.html", context)

def calculate_day_profit(request):

    todays_sold_tickets = SoldTickets.objects.filter(sold_date=date.today())
    sum = 0
    for i in todays_sold_tickets:
        sum += i.flyes_id.price
    print(sum)

    message = "Днейвная выручка составила : " + str(sum)

    context = {
        "title": "Расчет дневной выручки",
        "profile": profile,
        "todays_sold_tickets": todays_sold_tickets,
        "message": message
    }
    return render(request, "tickets/calculate_day_profit.html", context)

def profile(request):
    context = {
        "title": "Профиль",
    }

    if request.user.is_authenticated:

        profile = get_object_or_404(UserProfile, user=request.user)
        bought_tickets = profile.bought_tickets.all()
        form = ChangeBalanceForm(initial={'balance': profile.balance}, auto_id=False)

        if request.method == 'POST':
            form = ChangeBalanceForm(request.POST)
            if form.is_valid():
                profile.balance = form.cleaned_data["balance"]
                print(profile.balance)
                profile.save()

        context['profile'] = profile
        context['bought_tickets'] = bought_tickets
        context['form'] = form

    else:
        context['errors'] = ""
        return redirect('login')

    return render(request, "tickets/profile.html", context)




def add_flyght(request):
    if request.method == 'POST':
        form = AddFlyghtForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = AddFlyghtForm()

    context = {
        "title": "Рейс",
        "flight": flight,
        "form": form,
    }
    return render(request, "tickets/add_flyght.html", context)

def logout_user(request):
    logout(request)
    return redirect('login')

def lal(request, exeption):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

def registration(request, exeption):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

def login(request, exeption):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')