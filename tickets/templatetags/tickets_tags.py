from django import template
#from tickets.models import *

register = template.Library()

@register.simple_tag()
def get_menu():
    menu = [{"title": "Главная", "url_name": "home"},
            {"title": "Рейсы", "url_name": "allFlyes"},
            {"title": "Поиск рейса", "url_name": "flyght_search"},
            {"title": "Профиль", "url_name": "profile"},
            #{"title": "Логин", "url_name": "log_in"},
            #{"title": "Регистрация", "url_name": "sign_in"}
            ]
    return menu