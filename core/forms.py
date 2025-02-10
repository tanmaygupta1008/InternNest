# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from .models import User, JobListing

# # Signup Form for Job Seekers
# class JobSeekerSignUpForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']

# # Signup Form for Employers
# class EmployerSignUpForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']

# # Job Posting Form
# class JobListingForm(forms.ModelForm):
#     class Meta:
#         model = JobListing
#         fields = ['title', 'description', 'category', 'location', 'stipend', 'deadline', 'google_form_link']


# yourapp/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import (
    CustomUser, CandidateProfile, EmployerProfile, Category, Skill,
    Opportunity, Application, SavedOpportunity, Notification,
    Message, StaticPage, FAQ
)

#############################
# Custom User Forms
#############################

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'user_type', 'phone')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'user_type', 'phone')

#############################
# Candidate & Employer Profile Forms
#############################

class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        fields = ('resume_url', 'education', 'experience', 'skills', 'profile_summary', 'profile_picture')


class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = ('company_name', 'company_logo', 'description', 'website', 'location')

#############################
# Opportunity & Application Forms
#############################

class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = (
            'title', 'description', 'location', 'opportunity_type', 'salary_range',
            'stipend', 'duration', 'start_date', 'application_deadline', 'category',
            'skills_required', 'experience_required'
        )


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('resume_url', 'cover_letter')


class SavedOpportunityForm(forms.ModelForm):
    class Meta:
        model = SavedOpportunity
        # candidate and opportunity are set programmatically, so no fields are exposed
        fields = []

#############################
# Notification & Message Forms
#############################

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ('message', 'type', 'is_read')


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('receiver', 'content')

#############################
# Static Pages & FAQ Forms
#############################

class StaticPageForm(forms.ModelForm):
    class Meta:
        model = StaticPage
        fields = ('slug', 'title', 'content')


class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ('question', 'answer', 'order')


#############################
# Category & Skill Forms
#############################

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'description')


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ('name',)
