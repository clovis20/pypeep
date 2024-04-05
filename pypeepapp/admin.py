from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Peep, Profile

# Unregister Groups
admin.site.unregister(Group)

# Mix Profile Info into User Info
class ProfileInline(admin.StackedInline):
    model = Profile

# Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    # Just display username fields on admin page
    fields = ['username', 'first_name', 'last_name', 'email']
    inlines = [ProfileInline]

# Unregister initial User
admin.site.unregister(User)

# Register User and Profile
admin.site.register(User, UserAdmin)
#admin.site.register(Profile)
#admin.site.register(Profile)

# Register Peep
admin.site.register(Peep)