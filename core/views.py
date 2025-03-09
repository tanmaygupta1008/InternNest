# yourapp/views.py
from django.core.mail import send_mail
from django_otp.plugins.otp_email.models import EmailDevice
from .models import CustomUser  # Import your custom user model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import (
    CustomUserCreationForm, CustomUserChangeForm, 
    CandidateProfileForm, EmployerProfileForm, 
    OpportunityForm
)
from .models import CustomUser, CandidateProfile, EmployerProfile, Opportunity,JobApplication, CandidateProfile, ApplicationCounter
from django.http import JsonResponse

# ----------------------------
# Registration View
# ----------------------------
def home(request):
    opportunities = Opportunity.objects.all()
    return render(request, 'index11.html', {'opportunities': opportunities})

def register(request):
    """
    Handles new user registration.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Save the user instance
            user = form.save()

            # Create an EmailDevice for the user
            try:
                EmailDevice.objects.create(user=user, email=user.email, confirmed=True)
                messages.success(request, "Registration successful. You can now log in.")
            except Exception as e:
                messages.error(request, f"Failed to set up OTP device: {e}")

            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

# # ----------------------------
# # Login and Logout Views
# # ----------------------------


# def user_login(request):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         user_type = request.POST.get("user_type")
#         otp_code = request.POST.get("otp")  # Get the OTP if submitted

#         user = CustomUser.objects.filter(email=email).first()

#         if user:
#             if "get_otp" in request.POST:  # User clicked "Get OTP"
#                 # Authenticate with email and password
#                 user = authenticate(request, email=email, password=password)
#                 if user is not None:
#                     if user.user_type != user_type:
#                         messages.error(request, "User type does not match.")
#                         return redirect("login")

#                     # Generate OTP
#                     device, created = EmailDevice.objects.get_or_create(user=user, name="default")
#                     otp = device.generate_challenge()

#                     # Send OTP via email
#                     send_mail(
#                         "Your OTP Code",
#                         f"Your OTP code is {otp}",
#                         "no-reply@example.com",
#                         [user.email],
#                         fail_silently=False,
#                     )

#                     # Store user ID in session for OTP verification
#                     request.session["otp_user_id"] = user.id

#                     # Render login page again, now with OTP input field
#                     return render(request, "login.html", {"otp_sent": True, "email": email, "user_type": user_type})

#                 messages.error(request, "Invalid email or password.")
#                 return redirect("login")

#             elif "verify_otp" in request.POST:  # User submitted OTP
#                 user_id = request.session.get("otp_user_id")
#                 if not user_id:
#                     messages.error(request, "Session expired. Please try again.")
#                     return redirect("login")

#                 user = CustomUser.objects.get(id=user_id)
#                 device = EmailDevice.objects.filter(user=user, name="default").first()

#                 if device and device.verify_token(otp_code):
#                     login(request, user)  # Log the user in

#                     # Redirect based on user type
#                     return redirect("candidate_home" if user.user_type == "candidate" else "employer_home")
#                 else:
#                     messages.error(request, "Invalid OTP.")
#                     return render(request, "login.html", {"otp_sent": True, "email": email, "user_type": user_type})

#     return render(request, "login.html")
def user_login(request):
    if request.user.is_authenticated:
        user_type = request.user.user_type
        return redirect('candidate_home' if user_type == 'candidate' else 'employer_home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        # Handle "Get OTP" and "Resend OTP" buttons
        if 'get_otp' in request.POST or 'resend_otp' in request.POST:
            print("Resend OTP button clicked")
            # Use session data for Resend OTP if available
            email = request.session.get('email', email)
            password = request.session.get('password', password)
            user_type = request.session.get('user_type', user_type)

            user = authenticate(request, email=email, password=password)
            if user is not None and user.user_type == user_type:
                # Store session data
                request.session['email'] = email
                request.session['password'] = password
                request.session['user_type'] = user_type

                # Generate OTP
                device = user.emaildevice_set.first()
                if device:
                    device.generate_challenge()
                    if 'resend_otp' in request.POST:
                        messages.success(request, "OTP has been resent to your email.")
                    else:
                        messages.success(request, "OTP has been sent to your email.")
                    return redirect('login')

                messages.error(request, "OTP device not found.")
            else:
                messages.error(request, "Invalid credentials.")
            return redirect('login')

        # Handle "Verify OTP" button
        elif 'verify_otp' in request.POST:
            otp = request.POST.get('otp')
            email = request.session.get('email')  # Retrieve email from session
            password = request.session.pop('password', None)  # Remove password from session
            user_type = request.session.get('user_type')

            user = authenticate(request, email=email, password=password)
            if user is not None and user.user_type == user_type:
                device = user.emaildevice_set.first()
                if device and device.verify_token(otp):
                    login(request, user)
                    messages.success(request, "Login successful.")
                    return redirect('candidate_home' if user_type == 'candidate' else 'employer_home')
                else:
                    messages.error(request, "Invalid OTP.")
            else:
                messages.error(request, "Invalid credentials.")
            return redirect('login')

    return render(request, 'login.html')






def user_logout(request):
    logout(request)
    return redirect('login')


# ----------------------------
# Candidate Views
# ----------------------------
@login_required
def candidate_home(request):
    if request.user.user_type != 'candidate':
        return redirect('login')
    # For demonstration, you could load candidate applications, saved opportunities, etc.
    opportunities = Opportunity.objects.all()
    return render(request, 'candidate_home.html', {'opportunities': opportunities})

@login_required
def candidate_profile(request):
    # Ensure only candidates can access this view
    if request.user.user_type != 'candidate':
        return redirect('login')

    # Retrieve the candidate's profile or set it to None if it doesn't exist
    try:
        profile = request.user.candidate_profile
    except CandidateProfile.DoesNotExist:
        profile = None

    # Query all candidate profiles (if needed for the template)
    candidate_prof = CandidateProfile.objects.all()

    if request.method == 'POST':
        print("1")
        # Bind the form with POST data and files
        form = CandidateProfileForm(request.POST, request.FILES, instance=profile)
        print("POST data:", request.POST)

        if form.is_valid():
            print("2")
            print(form)
            # Save the form but don't commit yet
            candidate_profile = form.save(commit=False)
            candidate_profile.user = request.user
            request.user.first_name = form.cleaned_data.get('first_name')
            request.user.last_name = form.cleaned_data.get('last_name')
            request.user.save()
            
            candidate_profile.save()  # Save to the database
            print("Profile saved:", candidate_profile)

            # Add a success message
            messages.success(request, "Profile updated successfully.")
            return redirect('candidate_profile')
        else:
            # Print form errors for debugging
            print("Form is invalid. Errors:", form.errors)
    else:
        # Create a form instance pre-filled with the user's data
        form = CandidateProfileForm(instance=profile, user=request.user)

    # Render the form and any additional data
    return render(request, 'candidate_profile.html', {
        'form': form,
        'candidate_prof': candidate_prof,
    })


@login_required
def candidate_prof(request):
    if request.user.user_type != 'candidate':
        return redirect('login')
    try:
        profile = request.user.candidate_profile
    except CandidateProfile.DoesNotExist:
        profile = None
    candidate_prof=CandidateProfile.objects.all()
    candidate_profile = get_object_or_404(CandidateProfile, user=request.user)
    application_status = {
        "total_applications": JobApplication.objects.filter(candidate=candidate_profile).count(),
        "under_review": JobApplication.objects.filter(candidate=candidate_profile, status="Under_Review").count(),
        "shortlisted": JobApplication.objects.filter(candidate=candidate_profile, status="Shortlisted").count(),
        "hired": JobApplication.objects.filter(candidate=candidate_profile, status="Hired").count(),
        "rejected": JobApplication.objects.filter(candidate=candidate_profile, status="Rejected").count(),
        "applied": JobApplication.objects.filter(candidate=candidate_profile, status="Applied").count(),
    }
    recent_applications = JobApplication.objects.filter(candidate=candidate_profile)

    return render(request, 'candidate_prof.html', {
        "application_status": application_status,
        "recent_applications": recent_applications,
        'candidate_prof': candidate_prof,

    })
    

@login_required
def job_seeking(request):
    if request.user.user_type != 'candidate':
        return redirect('login')
    # List opportunities (jobs/internships) for candidates to view
    opportunities = Opportunity.objects.all()
    return render(request, 'job_seeking.html', {'opportunities': opportunities})

# ----------------------------
# Employer Views
# ----------------------------
# @login_required
# def employer_home(request):
#     if request.user.user_type != 'employer':
#         return redirect('login')
#     # For demonstration, load employer opportunities and applications
#     try:
#         profile = request.user.employer_profile
#     except EmployerProfile.DoesNotExist:
#         profile = None
#     opportunities = Opportunity.objects.filter(employer=profile) if profile else []
#     return render(request, 'employer_home.html', {'opportunities': opportunities})
@login_required
def employer_home(request):
    if request.user.user_type != 'employer':
        return redirect('login')
    
    try:
        profile = request.user.employer_profile
        opportunities = Opportunity.objects.filter(employer=profile)
        counters = profile.application_counter  # Fetch the counters for this employer
    except EmployerProfile.DoesNotExist:
        profile = None
        opportunities = []
        counters = None  # No counters if no profile exists
    
    return render(request, 'Emplyer-home.html', {
        'opportunities': opportunities,
        'counters': counters
    })


from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import json

@login_required
def employer_profile(request):
    if request.user.user_type != 'employer':
        return redirect('login')

    try:
        profile = request.user.employer_profile
    except EmployerProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = EmployerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
  
            employer_profile = form.save(commit=False)
            employer_profile.user = request.user

           # Parse achievements data from JSON
            achievements_json = request.POST.get('achievements', '[]')
            print("Achievements JSON:", achievements_json)
            try:
                achievements_data = json.loads(achievements_json)
                employer_profile.achievements = achievements_data
            except json.JSONDecodeError:
                employer_profile.achievements = []
            
            print("Achievements:", employer_profile.achievements)

            # employer_profile.company_url=request.POST.get("")

            # Handle social links
            employer_profile.social_links = {
                "linkedin": request.POST.get("social_links[linkedin]", ""),
                "twitter": request.POST.get("social_links[twitter]", ""),
                "facebook": request.POST.get("social_links[facebook]", ""),
            }

            # Handle logo upload
            if 'logo' in request.FILES:
                employer_profile.company_logo = request.FILES['logo']

            employer_profile.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('employer_profile')
    else:
        form = EmployerProfileForm(instance=profile)

    return render(request, 'Employeer-Profile-Editing.html', {'form': form, 'profile': profile})


@login_required
def employer_prof(request):
    if request.user.user_type != 'employer':
        return redirect('login')
    
    try:
        profile = request.user.employer_profile
        # Get all opportunities posted by this employer
        emprof = EmployerProfile.objects.all()
        opportunities = Opportunity.objects.filter(employer=profile)
    except EmployerProfile.DoesNotExist:
        profile = None
        opportunities = []
        emprof = None
    
    context = {
        'profile': profile,
        'emprof': emprof,
        'opportunities': opportunities,
    }
    return render(request, 'Profile-Employer.html', context)


from .models import Category
@login_required
def job_posting(request):
    if request.user.user_type != 'employer':
        return redirect('login')
    
    if request.method == 'POST':
        form = OpportunityForm(request.POST)
        if form.is_valid():
            opportunity = form.save(commit=False)
            try:
                opportunity.employer = request.user.employer_profile
            except EmployerProfile.DoesNotExist:
                messages.error(request, "Employer profile not found.")
                return redirect('employer_profile')
            
            opportunity.save()
            form.save_m2m()
            messages.success(request, "Job posted successfully.")
            return redirect('employer_home')
        else:
            print("Form errors:", form.errors)
    else:
        form = OpportunityForm()
    categories = Category.objects.all()  # Fetch categories
    return render(request, 'job_posting.html', {'form': form, 'categories': categories})



@login_required
def opportunity_detail(request, opportunity_id):
    opportunity = get_object_or_404(Opportunity, id=opportunity_id)
    return render(request, 'opportunity_detail.html', {'opportunity': opportunity})

@login_required
def opportunity_apply(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)
    if request.method == 'POST':
        candidate_profile = get_object_or_404(CandidateProfile, user=request.user)
        resume_url = request.POST.get('resume_url')
        pdf_file = request.FILES.get('pdf_file')
        print("PDF file:", pdf_file)
        cover_letter = request.POST.get('cover_letter')

        # Create the application
        JobApplication.objects.create(
            opportunity=opportunity,
            candidate=candidate_profile,
            pdf_file=pdf_file,
            resume_url=resume_url,
            cover_letter=cover_letter,
        )
        return redirect('candidate_prof')  # Redirect to a success page or dashboard

    return render(request, 'opportunity_apply.html', {'opportunity': opportunity})



def search_list(request):
    # Fetch all job opportunities, candidates, and employers
    opportunities = Opportunity.objects.all()
    candidates = CandidateProfile.objects.select_related('user').all()
    employers = EmployerProfile.objects.select_related('user').all()

    # Pass the data to the template
    context = {
        'opportunities': opportunities,
        'candidates': candidates,
        'employers': employers,
    }
    return render(request, 'search.html', context)

def view_profile(request, user_id):
    """
    View for displaying a user's profile
    """
    profile = get_object_or_404(CandidateProfile, id=user_id)
    return render(request, 'view_profile.html', {'profile': profile})

def view_employer_profile(request, employer_id):
    """
    View for displaying an employer's profile
    """
    employer = get_object_or_404(EmployerProfile, id=employer_id)
    return render(request, 'view_employer_profile.html', {'employer': employer})



@login_required  # Ensure the user is logged in
def dashboard(request):
    # Fetch the logged-in user's name
    user_name = request.user.get_full_name() or request.user.username  # Use full name or fallback to username
    context = {
        'user_name': user_name,
    }
    return render(request, 'Dashboard-Employer.html', context)


@login_required  # Ensure the user is logged in
def employer_applications(request):
    # Fetch the logged-in user's name and employer profile
    user = request.user
    employer_profile = user.employer_profile
    user_name = user.get_full_name() or user.username

    # Get status filter from URL parameter or default to 'all'
    status_filter = request.GET.get('status', 'all')
    
    # Get all applications for opportunities posted by this employer
    applications = JobApplication.objects.filter(
        opportunity__employer=employer_profile
    ).select_related('opportunity', 'candidate', 'candidate__user').order_by('-applied_at')
    
    # Apply status filter if not 'all'
    if status_filter != 'all':
        applications = applications.filter(status=status_filter)
    
    # Get application counts for each status
    status_counts = {
        'all': applications.count(),
        'applied': applications.filter(status='applied').count(),
        'under_review': applications.filter(status='under_review').count(),
        'shortlisted': applications.filter(status='shortlisted').count(),
        'rejected': applications.filter(status='rejected').count(),
        'hired': applications.filter(status='hired').count(),
    }

    context = {
        'user_name': user_name,
        'applications': applications,
        'current_status': status_filter,
        'status_counts': status_counts,
    }
    return render(request, 'employer_applications.html', context)

@login_required
def update_application_status(request):
    if request.method == 'POST':
        application_id = request.POST.get('application_id')
        new_status = request.POST.get('status')
        
        try:
            application = JobApplication.objects.get(id=application_id, 
                                                   opportunity__employer=request.user.employer_profile)
            
            # Update application status
            old_status = application.status
            application.status = new_status
            application.save()
            
            # # Update counter
            # ApplicationCounter.update_counters(application.opportunity.employer, old_status, new_status)
            
            return JsonResponse({'status': 'success'})
        except JobApplication.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Application not found'}, status=404)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
