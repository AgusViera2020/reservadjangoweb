from django.contrib import admin
from .models import CustomUser, Profile
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm


admin.site.register(CustomUser)
admin.site.register(Profile)


#mix profile info and user info
class ProfileInLine(admin.StackedInline):
    model = Profile

"""class CustomUserAdmin(UserAdmin):
    add_form= CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['nombre','apellido','email','password', 'telefono']
    inlines = [ProfileInLine]"""

class UserAdmin(admin.ModelAdmin):
    model = CustomUser
    field = ['nombre', 'apellido','email','password','telefono']
    inlines = [ProfileInLine]


admin.site.unregister(CustomUser)
admin.site.register(CustomUser,UserAdmin)