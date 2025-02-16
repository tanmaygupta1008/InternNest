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
    Opportunity, JobApplication, SavedOpportunity, Notification,
    Message, StaticPage, FAQ , ApplicationCounter
)
from datetime import date

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
        fields = ('resume_url', 'education', 'experience', 'skills', 'profile_summary', 'profile_picture', 'birthdate','currently')
  
    widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
            'currently': forms.Select(choices=CandidateProfile.EMPLOYMENT_STATUS_CHOICES),
        }
    def clean_education(self):
        education_data = {}
        for key, value in self.data.items():
            if key.startswith('education['):
                # Extract the index and field name
                index = int(key.split('[')[1].split(']')[0])
                field = key.split('[')[2].split(']')[0]

                # Group the data by index
                if index not in education_data:
                    education_data[index] = {}
                education_data[index][field] = value

        # Convert grouped data into a list of dictionaries
        education_list = [entry for entry in education_data.values()]

        # Validate the entries
        for entry in education_list:
            if not all(key in entry for key in ['degree', 'institution', 'end_year']):
                raise forms.ValidationError("Each education entry must have a degree, institution, and end year.")
        return education_list

    def clean_skills(self):
        skills = self.data.getlist('skills[]')
        if not skills:
            raise forms.ValidationError("Skills cannot be empty.")
        return skills

    def clean_experience(self):
     experience_data = {}
     for key, value in self.data.items():
        if key.startswith('experience['):
            index = int(key.split('[')[1].split(']')[0])
            field = key.split('[')[2].split(']')[0]

            if index not in experience_data:
                experience_data[index] = {}
            experience_data[index][field] = value

     # Convert grouped data into a list of dictionaries
     experience_list = [entry for entry in experience_data.values()]

     # Validate each entry
     for entry in experience_list:
        if not all(key in entry for key in ['company', 'position', 'start_date', 'end_date']):
            raise forms.ValidationError("Each experience entry must include company, position, start date, and end date.")
     return experience_list


    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('birthdate')

        if not birthdate:
            return None  # Allow empty birthdate if it's optional
        
        # Optional: Ensure the birthdate is not in the future
        if birthdate > date.today():
            raise forms.ValidationError("Birthdate cannot be in the future.")
        
        return birthdate


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
