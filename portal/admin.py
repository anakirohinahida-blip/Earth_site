from  .models import Client, Application
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin


class ClientInline(admin.StackedInline):
    model = Client
    can_delete = False


class CustomUserAdmin(UserAdmin):
    inlines = (ClientInline,)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('client', 'building', 'plot_size', 'status')
    list_filter = ('status',)

    actions = ['mark_in_progress']

    def mark_in_progress(self, request, queryset):
        queryset.update(status = 'in_progres')
    mark_in_progress.short_description = 'Отметить как "Подтверждено"'

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'user')

