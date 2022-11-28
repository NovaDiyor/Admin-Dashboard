from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'is_active']
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_('Extra'), {'fields': ('status', 'number')}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )


admin.site.register(Info)
admin.site.register(Ads)
admin.site.register(Slider)
admin.site.register(Report)
admin.site.register(League)
admin.site.register(Club)
admin.site.register(Player)
admin.site.register(Game)
admin.site.register(Substitute)
admin.site.register(Line)
admin.site.register(Goal)
admin.site.register(Passes)
admin.site.register(Statics)
admin.site.register(Table)
admin.site.register(Detail)
admin.site.register(Product)
admin.site.register(Wishlist)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Chat)
admin.site.register(Telegram)
