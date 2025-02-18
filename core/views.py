# from django.shortcuts import render, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from .models import JobInternshipPosting, Application

# @login_required
# def home(request):
#     if request.user.user_type == 'normal':
#         # Normal user dashboard
#         applications = Application.objects.filter(user=request.user)
#         return render(request, 'core/normal_user_dashboard.html', {'applications': applications})
#     else:
#         # Employer dashboard
#         postings = JobInternshipPosting.objects.filter(employer=request.user)
#         return render(request, 'core/employer_dashboard.html', {'postings': postings})

# @login_required
# def job_internship_detail(request, posting_id):
#     posting = get_object_or_404(JobInternshipPosting, id=posting_id)
#     return render(request, 'core/job_internship_detail.html', {'posting': posting})

# @login_required
# def apply(request, posting_id):
#     if request.method == 'POST':
#         posting = get_object_or_404(JobInternshipPosting, id=posting_id)
#         Application.objects.create(
#             posting=posting,
#             user=request.user,
#             cover_letter_url=request.POST.get('cover_letter_url'),
#             resume_url=request.POST.get('resume_url')
#         )
#         return redirect('home')
#     return render(request, 'core/apply.html', {'posting_id': posting_id})
# from django.shortcuts import render, redirect
# from django.contrib.auth import login
# from .models import JobListing
# from .forms import JobSeekerSignUpForm, EmployerSignUpForm, JobListingForm

# # Homepage
# def home(request):
#     jobs = JobListing.objects.all()
#     return render(request, 'home.html', {'jobs': jobs})

# # Job Seeker Registration
# def job_seeker_register(request):
#     if request.method == "POST":
#         form = JobSeekerSignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_employer = False
#             user.save()
#             login(request, user)
#             return redirect('home')
#     else:
#         form = JobSeekerSignUpForm()
#     return render(request, 'register.html', {'form': form})

# # Employer Registration
# def employer_register(request):
#     if request.method == "POST":
#         form = EmployerSignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_employer = True
#             user.save()
#             login(request, user)
#             return redirect('home')
#     else:
#         form = EmployerSignUpForm()
#     return render(request, 'register.html', {'form': form})

# # Job Posting (For Employers)
# def post_job(request):
#     if request.method == "POST":
#         form = JobListingForm(request.POST)
#         if form.is_valid():
#             job = form.save(commit=False)
#             job.employer = request.user
#             job.save()
#             return redirect('home')
#     else:
#         form = JobListingForm()
#     return render(request, 'post_job.html', {'form': form})

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
            user = form.save()  # Save the user instance
            messages.success(request, "Registration successful. You can now log in.")
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
        "under_review": JobApplication.objects.filter(candidate=candidate_profile, status="Under Review").count(),
        "shortlisted": JobApplication.objects.filter(candidate=candidate_profile, status="Shortlisted").count(),
    }
    recent_applications = JobApplication.objects.filter(candidate=candidate_profile).order_by('-applied_at')[:5]

    return render(request, 'candidate_prof.html', {
        "application_status": application_status,
        "recent_applications": recent_applications,
        'candidate_prof': candidate_prof
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
@login_required
def employer_home(request):
    if request.user.user_type != 'employer':
        return redirect('login')
    # For demonstration, load employer opportunities and applications
    try:
        profile = request.user.employer_profile
    except EmployerProfile.DoesNotExist:
        profile = None
    opportunities = Opportunity.objects.filter(employer=profile) if profile else []
    return render(request, 'employer_home.html', {'opportunities': opportunities})


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
            employer_profile.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('employer_profile')
    else:
        form = EmployerProfileForm(instance=profile)
    return render(request, 'employer_profile.html', {'form': form})


@login_required
def job_posting(request):
    if request.user.user_type != 'employer':
        return redirect('login')
    if request.method == 'POST':
        form = OpportunityForm(request.POST)
        if form.is_valid():
            opportunity = form.save(commit=False)
            # Assign the employer profile to the opportunity
            try:
                opportunity.employer = request.user.employer_profile
            except EmployerProfile.DoesNotExist:
                messages.error(request, "Employer profile not found.")
                return redirect('employer_profile')
            opportunity.save()
            # ManyToMany relationships need to be saved after saving the instance
            form.save_m2m()
            messages.success(request, "Job posted successfully.")
            return redirect('employer_home')
    else:
        form = OpportunityForm()
    return render(request, 'job_posting.html', {'form': form})

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
        cover_letter = request.POST.get('cover_letter')

        # Create the application
        JobApplication.objects.create(
            opportunity=opportunity,
            candidate=candidate_profile,
            resume_url=resume_url,
            cover_letter=cover_letter,
        )

        # Increment the applied counter
        ApplicationCounter.increment(opportunity.employer, 'applied')
        return redirect('candidate_prof')  # Redirect to a success page or dashboard

    return render(request, 'opportunity_apply.html', {'opportunity': opportunity})

