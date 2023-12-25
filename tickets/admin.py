from django.contrib import admin


from .models import Flyes, SoldTickets, UserProfile

class FlyesAdmin(admin.ModelAdmin):
    list_display = ('id', 'arrival', 'departure', 'arrival_date', 'departure_date', 'price', 'quantity')
    list_display_links = ('id', 'arrival')
    search_fields = ('arrival', )
    list_editable = ('quantity', )
    list_filter = ('price',)

class SoldTicketsAdmin(admin.ModelAdmin):
    list_display = ('id', 'flyes_id', 'user_id', 'place_number')
    list_display_links = ('id', 'flyes_id', 'user_id')
    search_fields = ('id', )
    list_editable = ('place_number', )
    #list_filter = ('price',)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'balance')


admin.site.register(Flyes, FlyesAdmin)
admin.site.register(SoldTickets, SoldTicketsAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

# Register your models here.
