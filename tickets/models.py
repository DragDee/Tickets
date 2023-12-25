from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date


class Flyes(models.Model):
    arrival = models.CharField(max_length=255)
    departure = models.CharField(max_length=255)
    departure_date = models.DateTimeField()
    arrival_date = models.DateTimeField()
    price = models.FloatField()
    quantity = models.IntegerField()

    def __str__(self):
        s = self.arrival + "/" + self.departure
        return s

    def get_absolute_url(self):
        return reverse('flight', kwargs={'flightid': self.pk})

    def get_buy_ticket_url(self):
        return reverse('buy_ticket', kwargs={'flight_id': self.pk})

    class Meta:
        verbose_name = "Таблица рейсов"
        verbose_name_plural = "Таблица рейсов"
        ordering = ['arrival']



class SoldTickets(models.Model):
    flyes_id = models.ForeignKey('Flyes', on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    place_number = models.IntegerField()
    sold_date = models.DateField(default=date.today())
    cashier = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('refund', kwargs={'ticket_id': self.id})
# Create your models here.

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)
    bought_tickets = models.ManyToManyField(SoldTickets)

    class Meta:
        verbose_name = "Profile"
