# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('posting/<int:posting_id>/', views.job_internship_detail, name='job_internship_detail'),
#     path('apply/<int:posting_id>/', views.apply, name='apply'),
# ]
# from django.urls import path
# from . import views

# urlpatterns = [
# #     path('', views.home, name='home'),
# #     path('register/job_seeker/', views.job_seeker_register, name='job_seeker_register'),
# #     path('register/employer/', views.employer_register, name='employer_register'),
# #     path('post-job/', views.post_job, name='post_job'),
# ]

# yourapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # Auth URLs
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Candidate URLs
    path('candidate/home/', views.candidate_home, name='candidate_home'),
    path('candidate/profile/', views.candidate_profile, name='candidate_profile'),
    path('candidate/prof/', views.candidate_prof, name='candidate_prof'),
    path('jobs/', views.job_seeking, name='job_seeking'),
    path('opportunity/<int:opportunity_id>/', views.opportunity_detail, name='opportunity_detail'),
    
    
    # Employer URLs
    path('employer/home/', views.employer_home, name='employer_home'),
    path('employer/profile/', views.employer_profile, name='employer_profile'),
    path('employer/job-posting/', views.job_posting, name='job_posting'),
    path('opportunity_apply/<int:pk>/', views.opportunity_apply, name='opportunity_apply'),
]
