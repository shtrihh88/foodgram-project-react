from django.contrib import admin
from users.models import Follow, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'email', 'first_name', 'last_name', 'password',
    )
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
    list_filter = ('user', 'author')
    empty_value_display = '-пусто-'
