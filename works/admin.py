from django.contrib import admin

from .models import Address, Work

# Register your models here.


admin.site.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('street', 'number', 'complement', 'neighborhood', 'city', 'state', 'cep')
    search_fields = ('street',)


admin.site.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'client', 'phone')
    search_fields = ('name',)