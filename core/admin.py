# from django.contrib import admin
# from .models import JobListing, User, EmployerProfile, JobSeekerProfile, Application
# # Register your models here.
# admin.site.register(JobListing)
# admin.site.register(User)
# admin.site.register(EmployerProfile)
# admin.site.register(JobSeekerProfile)
# admin.site.register(Application)

# yourapp/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    CustomUser, CandidateProfile, EmployerProfile, Category, Skill,
    Opportunity, Application, SavedOpportunity, Notification,
    Message, StaticPage, FAQ
)
from .forms import CustomUserCreationForm, CustomUserChangeForm

#############################
# Custom User Admin
#############################

class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'user_type')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'user_type', 'phone', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


#############################
# Register Models with Admin
#############################

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CandidateProfile)
admin.site.register(EmployerProfile)
admin.site.register(Category)
admin.site.register(Skill)
admin.site.register(Opportunity)
admin.site.register(Application)
admin.site.register(SavedOpportunity)
admin.site.register(Notification)
admin.site.register(Message)
admin.site.register(StaticPage)
admin.site.register(FAQ)