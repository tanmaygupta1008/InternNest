# from django.contrib.auth.models import AbstractUser
# from django.db import models

# class User(AbstractUser):
#     USER_TYPES = (
#         ('normal', 'Normal User'),
#         ('employer', 'Employer'),
#     )
#     user_type = models.CharField(max_length=10, choices=USER_TYPES, default='normal')
#     groups = models.ManyToManyField(
#         'auth.Group',
#         related_name='custom_user_set',  # Add this line
#         blank=True,
#         help_text='The groups this user belongs to.',
#         verbose_name='groups',
#     )
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         related_name='custom_user_permissions_set',  # Add this line
#         blank=True,
#         help_text='Specific permissions for this user.',
#         verbose_name='user permissions',
#     )

# class NormalUserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='normal_profile')
#     full_name = models.CharField(max_length=100)
#     phone_number = models.CharField(max_length=15)
#     resume_url = models.URLField(blank=True, null=True)
#     skills = models.JSONField(default=list)
#     education = models.JSONField(default=list)
#     profile_picture_url = models.URLField(blank=True, null=True)
#     location = models.CharField(max_length=100)

#     def __str__(self):
#         return self.full_name

# class EmployerProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer_profile')
#     company_name = models.CharField(max_length=100)
#     company_description = models.TextField()
#     company_logo_url = models.URLField(blank=True, null=True)
#     website_url = models.URLField(blank=True, null=True)
#     location = models.CharField(max_length=100)

#     def __str__(self):
#         return self.company_name

# class Skill(models.Model):
#     name = models.CharField(max_length=100, unique=True)

#     def __str__(self):
#         return self.name

# class JobInternshipPosting(models.Model):
#     POSTING_TYPES = (
#         ('job', 'Job'),
#         ('internship', 'Internship'),
#     )
#     employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='postings')
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     type = models.CharField(max_length=10, choices=POSTING_TYPES)
#     location = models.CharField(max_length=100)
#     start_date = models.DateField()
#     duration = models.CharField(max_length=50, blank=True, null=True)  # For internships
#     stipend = models.CharField(max_length=50, blank=True, null=True)  # For internships
#     salary = models.CharField(max_length=50, blank=True, null=True)  # For jobs
#     skills_required = models.ManyToManyField(Skill)
#     application_deadline = models.DateField()
#     posted_at = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive'), ('closed', 'Closed')], default='active')

#     def __str__(self):
#         return self.title

# class Application(models.Model):
#     STATUS_CHOICES = (
#         ('pending', 'Pending'),
#         ('accepted', 'Accepted'),
#         ('rejected', 'Rejected'),
#     )
#     posting = models.ForeignKey(JobInternshipPosting, on_delete=models.CASCADE, related_name='applications')
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
#     applied_at = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
#     cover_letter_url = models.URLField(blank=True, null=True)
#     resume_url = models.URLField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.posting.title}"

# from django.db import models
# from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import Group, Permission

# # Custom User Model (For Job Seekers & Employers)
# # Custom User Model (For Job Seekers & Employers)
# class User(AbstractUser):
#     is_employer = models.BooleanField(default=False)
#     groups = models.ManyToManyField(Group, related_name='custom_user_set')
#     user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set_permissions')

# # Employer Profile
# class EmployerProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     company_name = models.CharField(max_length=255)
#     company_website = models.URLField(blank=True, null=True)

#     def __str__(self):
#         return self.company_name

# # Job Seeker Profile
# class JobSeekerProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     resume = models.FileField(upload_to='resumes/', blank=True, null=True)
#     skills = models.TextField()

#     def __str__(self):
#         return self.user.username

# # Internships/Jobs
# class JobListing(models.Model):
#     employer = models.ForeignKey(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     category = models.CharField(max_length=255)
#     location = models.CharField(max_length=255, blank=True, null=True)
#     stipend = models.CharField(max_length=100, blank=True, null=True)
#     deadline = models.DateField()
#     google_form_link = models.URLField()

#     def __str__(self):
#         return self.title

# # Applications (Tracking who applied where)
# class Application(models.Model):
#     job_seeker = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
#     job_listing = models.ForeignKey(JobListing, on_delete=models.CASCADE,default=None)
#     applied_on = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.job_seeker.username} applied for {self.job_listing.title}"


# yourapp/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

##############################
# Custom User Model & Manager
##############################

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
            
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom user model where email is the unique identifier.
    """
    username = None  # remove the username field
    email = models.EmailField(unique=True)
    USER_TYPE_CHOICES = (
        ('candidate', 'Candidate'),
        ('employer', 'Employer'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'user_type']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

#################################
# Profile Tables for Each User
#################################

class CandidateProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='candidate_profile')
    resume_url = models.URLField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    # You might want to store skills as JSON or a comma‐separated list. Alternatively, see the ManyToMany below.
    skills = models.TextField(blank=True, null=True)
    profile_summary = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}'s Candidate Profile"


class EmployerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employer_profile')
    company_name = models.CharField(max_length=255)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

###########################
# Supporting Tables
###########################

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

###########################
# Opportunities (Jobs/Internships)
###########################

class Opportunity(models.Model):
    OPPORTUNITY_TYPE_CHOICES = (
        ('job', 'Job'),
        ('internship', 'Internship'),
    )
    employer = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE, related_name='opportunities')
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    opportunity_type = models.CharField(max_length=20, choices=OPPORTUNITY_TYPE_CHOICES)
    salary_range = models.CharField(max_length=100, blank=True, null=True)
    stipend = models.CharField(max_length=100, blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    application_deadline = models.DateField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    # Using a ManyToManyField to Skill. This works as a pivot table automatically.
    skills_required = models.ManyToManyField(Skill, blank=True, related_name='opportunities')
    experience_required = models.CharField(max_length=100, blank=True, null=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

###########################
# Applications
###########################

class Application(models.Model):
    STATUS_CHOICES = (
        ('applied', 'Applied'),
        ('reviewed', 'Reviewed'),
        ('interview', 'Interview'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
    )
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='applications',default=None)
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='applications',default=None)
    resume_url = models.URLField(blank=True, null=True)
    cover_letter = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.candidate.user.email} - {self.opportunity.title}"

###########################
# Saved Opportunities
###########################

class SavedOpportunity(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='saved_opportunities')
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('candidate', 'opportunity')

    def __str__(self):
        return f"{self.candidate.user.email} saved {self.opportunity.title}"

###########################
# Notifications
###########################

class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    type = models.CharField(max_length=50, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Notification for {self.user.email}"

###########################
# Messaging
###########################

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"Message from {self.sender.email} to {self.receiver.email}"

###########################
# Static Pages & FAQs
###########################

class StaticPage(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title


class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.question
