from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class CustomUserAdmin(UserAdmin):
    # Какие поля отображаются в списке пользователей
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

    # Фильтры в правой части админки
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    # Поля, по которым работает поиск
    search_fields = ('username', 'email', 'first_name', 'last_name')

    # Сортировка по умолчанию
    ordering = ('username',)


# Сначала отменяем стандартную регистрацию
admin.site.unregister(User)

# Регистрируем с новым классом админки
admin.site.register(User, CustomUserAdmin)