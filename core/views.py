from django.shortcuts import render, redirect, get_object_or_404
from .models import StudyMaterial, University, Course, YearSemester ,Student , QuestionPaper, Notification
from .forms import StudyMaterialForm ,StudentSignUpForm, StudentProfileForm ,QuestionPaperForm ,PasswordChangeForm ,ProfileUpdateForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.forms import modelform_factory
from django.http import HttpResponseForbidden ,JsonResponse
from django.contrib.auth import login, authenticate , logout ,update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models import Q
from django.db.models import Count
from django.db.models.functions import TruncMonth
from .serializers import StudentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.admin.views.decorators import staff_member_required

def home_redirect_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    elif hasattr(request.user, 'student'):
        return redirect('choose_content')
    elif request.user.is_staff:
        return redirect('dashboard')
    else:
        return redirect('login')  # Default fallback

@login_required
def dashboard(request):
    # Fetch all filter options
    universities = University.objects.all()
    courses = Course.objects.all()
    years = YearSemester.objects.all()

    # --------------------
    # Study Material Filters
    # --------------------
    mat_title = request.GET.get('mat_title', '')
    mat_university = request.GET.get('mat_university', '')
    mat_course = request.GET.get('mat_course', '')
    mat_year = request.GET.get('mat_year', '')
    mat_subject = request.GET.get('mat_subject', '')

    materials = StudyMaterial.objects.all()
    if mat_title:
        materials = materials.filter(title__icontains=mat_title)
    if mat_university:
        materials = materials.filter(university_id=mat_university)
    if mat_course:
        materials = materials.filter(course_id=mat_course)
    if mat_year:
        materials = materials.filter(year_or_semester_id=mat_year)
    if mat_subject:
        materials = materials.filter(subject__icontains=mat_subject)

    available_subjects = StudyMaterial.objects.values_list('subject', flat=True).distinct()

    # --------------------
    # Student Filters
    # --------------------
    stu_university = request.GET.get('stu_university', '')
    stu_course = request.GET.get('stu_course', '')
    stu_year = request.GET.get('stu_year', '')

    students = Student.objects.all()
    if stu_university:
        students = students.filter(university_id=stu_university)
    if stu_course:
        students = students.filter(course_id=stu_course)
    if stu_year:
        students = students.filter(year_or_semester_id=stu_year)

    # --------------------
    # Question Paper Filters
    # --------------------
    qp_title = request.GET.get('qp_title', '')
    qp_university = request.GET.get('qp_university', '')
    qp_course = request.GET.get('qp_course', '')
    qp_year = request.GET.get('qp_year', '')
    qp_subject = request.GET.get('qp_subject', '')
    
    question_papers = QuestionPaper.objects.all()
    if qp_title:
        question_papers = question_papers.filter(title__icontains=qp_title)
    if qp_university:
        question_papers = question_papers.filter(university_id=qp_university)
    if qp_course:
        question_papers = question_papers.filter(course_id=qp_course)
    if qp_year:
        question_papers = question_papers.filter(year_or_semester_id=qp_year)
    if qp_subject:
        question_papers = question_papers.filter(subject__icontains=qp_subject)
    available_qp_subjects = QuestionPaper.objects.values_list('subject', flat=True).distinct()
    # --------------------
    # Monthly Registration Stats
    # --------------------
    registrations = Student.objects.annotate(month=TruncMonth('registration_date')) \
        .values('month') \
        .annotate(reg_count=Count('id')) \
        .order_by('month')

    months = [r['month'].strftime('%b %Y') for r in registrations]
    student_counts = [r['reg_count'] for r in registrations]

    # --------------------
    # Notifications
    # --------------------
    notifications = Notification.objects.order_by('-timestamp')[:10]

    # --------------------
    # Context
    # --------------------
    context = {
        # Filters
        'universities': universities,
        'courses': courses,
        'years': years,

        # Study Material
        'materials': materials,
        'mat_title': mat_title,
        'mat_university': mat_university,
        'mat_course': mat_course,
        'mat_year': mat_year,
        'mat_subject': mat_subject,
        'available_subjects': available_subjects,

        # Students
        'students': students,
        'stu_university': stu_university,
        'stu_course': stu_course,
        'stu_year': stu_year,

        # Question Papers
        'question_papers': question_papers,
        'qp_title': qp_title,
        'qp_university': qp_university,
        'qp_course': qp_course,
        'qp_year': qp_year,
        'qp_subject': qp_subject,
        'available_qp_subjects': available_qp_subjects,

        # Stats
        'months': months,
        'student_counts': student_counts,

        # Notifications
        'notifications': notifications,
    }

    # Handle AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'dashboard.html', context)

    return render(request, 'dashboard.html', context)

# Upload Material View
@login_required
def upload_material(request):
    # Make sure only staff/teachers can access this view
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to perform this action.")
    
    

    if request.method == 'POST':
        form = StudyMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Study material uploaded successfully.")
            return redirect('dashboard')
    else:
        form = StudyMaterialForm()
    return render(request, 'upload.html', {'form': form})



@login_required
def upload_question_paper(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to perform this action.")

    if request.method == 'POST':
        form = QuestionPaperForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Question paper uploaded successfully.")
            return redirect('dashboard')
    else:
        form = QuestionPaperForm()
    return render(request, 'upload.html', {'form': form, 'title': 'Upload Question Paper'})


@login_required
def edit_question_paper(request, pk):
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to perform this action.")

    question_paper = get_object_or_404(QuestionPaper, pk=pk)

    if request.method == 'POST':
        form = QuestionPaperForm(request.POST, request.FILES, instance=question_paper)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to the dashboard after successful edit
    else:
        form = QuestionPaperForm(instance=question_paper)

    return render(request, 'edit_question_paper.html', {'form': form, 'title': 'Edit Question Paper'})

# View to delete a question paper
@login_required
def delete_question_paper(request, pk):
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to perform this action.")
    
    question_paper = get_object_or_404(QuestionPaper, pk=pk)

    if request.method == 'POST':
        question_paper.delete()
        return redirect('dashboard')  # Redirect to the dashboard after successful deletion

    return render(request, 'delete_question_paper.html', {'question_paper': question_paper, 'title': 'Delete Question Paper'})


# Edit Material View
@login_required
def edit_material(request, pk):
    # Make sure only staff/teachers can access this view
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to perform this action.")

    material = get_object_or_404(StudyMaterial, pk=pk)
    form = StudyMaterialForm(request.POST or None, request.FILES or None, instance=material)
    if form.is_valid():
        form.save()
        return redirect('dashboard')
    return render(request, 'upload.html', {'form': form, 'edit': True})

# Delete Material View
@login_required
def delete_material(request, pk):
    # Make sure only staff/teachers can access this view
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to perform this action.")

    material = get_object_or_404(StudyMaterial, pk=pk)
    material.delete()
    return redirect('dashboard')

# Add University View
@login_required
def add_university(request):
    # Make sure only staff/teachers can access this view
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to perform this action.")

    UniversityForm = modelform_factory(University, fields=["name"])
    form = UniversityForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('upload')
    return render(request, 'simple_add.html', {'form': form, 'title': 'Add University'})

# Add Course View
@login_required
def add_course(request):
    # Make sure only staff/teachers can access this view
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to perform this action.")

    CourseForm = modelform_factory(Course, fields=["name"])
    form = CourseForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('upload')
    return render(request, 'simple_add.html', {'form': form, 'title': 'Add Course'})

# Add Year/Semester View
@login_required
def add_yearsemester(request):
    # Make sure only staff/teachers can access this view
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to perform this action.")

    YearForm = modelform_factory(YearSemester, fields=["name"])
    form = YearForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('upload')
    return render(request, 'simple_add.html', {'form': form, 'title': 'Add Year/Semester'})


def student_signup(request):
    if request.method == 'POST':
        user_form = StudentSignUpForm(request.POST)
        profile_form = StudentProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            # Create user and save
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            # Create Student profile and save
            student_profile = profile_form.save(commit=False)
            student_profile.user = user
            student_profile.save()

            Notification.objects.create(
                message=f"New student registered: {student_profile.user}"
            )
            # Explicitly authenticate using the correct backend
            user = authenticate(request, username=user.email, password=user_form.cleaned_data['password'], backend='core.backends.EmailBackend')

            if user is not None:
                login(request, user)

                # Redirect the student to their profile or home page, not the dashboard
                return redirect('choose_content')  # Redirect to a page where students can go
            else:
                messages.error(request, "Authentication failed after signup.")
        else:
            messages.error(request, "Form is invalid.")
    else:
        user_form = StudentSignUpForm()
        profile_form = StudentProfileForm()

    return render(request, 'student_signup.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def edit_student(request, student_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = StudentProfileForm(instance=student)

    return render(request, 'edit_student.html', {'form': form})

@login_required
def delete_student(request, student_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return redirect('dashboard')

@login_required
def add_student(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to perform this action.")

    if request.method == 'POST':
        user_form = StudentSignUpForm(request.POST)
        profile_form = StudentProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            student = profile_form.save(commit=False)
            student.user = user
            student.save()
            messages.success(request, "Student added successfully.")
            return redirect('dashboard')
    else:
        user_form = StudentSignUpForm()
        profile_form = StudentProfileForm()

    return render(request, 'add_student.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def choose_content(request):
    if not hasattr(request.user, 'student'):
        return HttpResponseForbidden("Student profile not found.")

    student = request.user.student

    return render(request, 'choose_content.html', {
        'student': student
    })

@login_required
def student_materials(request):
    student = Student.objects.get(user=request.user)

    # Base queryset
    materials = StudyMaterial.objects.filter(
        university=student.university,
        course=student.course,
        year_or_semester=student.year_or_semester
    )

    # Distinct subjects for the dropdown
    available_subjects = materials.values_list('subject', flat=True).distinct()

    # Filter by search query
    query = request.GET.get('q')
    if query:
        materials = materials.filter(
            Q(title__icontains=query) | Q(subject__icontains=query)
        )

    # Filter by semester
    semester = request.GET.get('semester')
    if semester:
        materials = materials.filter(semester=semester)

    # Filter by subject
    subject = request.GET.get('subject')
    if subject:
        materials = materials.filter(subject=subject)

    # Handle AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        materials_data = [
            {
                'title': material.title,
                'subject': material.subject,
                'file_url': material.file_upload.url if material.file_upload else None,
                'drive_link': material.drive_link,
                'material_id': material.id,
            }
            for material in materials
        ]
        return JsonResponse({'materials': materials_data})

    return render(request, 'student_materials.html', {
        'student': student,
        'materials': materials,
        'available_subjects': available_subjects,
        'selected_semester': semester or '',
        'selected_subject': subject or ''
    })


@login_required
def student_question_papers(request):
    student = Student.objects.get(user=request.user)

    # Base queryset filtered by student details
    question_papers = QuestionPaper.objects.filter(
        university=student.university,
        course=student.course,
        year_or_semester=student.year_or_semester
    )

    # Get list of distinct subjects for the filter
    available_subjects = question_papers.values_list('subject', flat=True).distinct()

    # Filter by search query
    query = request.GET.get('q')
    if query:
        question_papers = question_papers.filter(
            Q(title__icontains=query) | Q(subject__icontains=query)
        )

    # Filter by semester (string: "I", "II", etc.)
    semester = request.GET.get('semester')
    if semester:
        question_papers = question_papers.filter(semester=semester)

    # Filter by subject
    subject = request.GET.get('subject')
    if subject:
        question_papers = question_papers.filter(subject=subject)

    # AJAX request handling
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        papers_data = [
            {
                'title': q.title,
                'file_url': q.file_upload.url if q.file_upload else None,
                'drive_link': q.drive_link,
                'question_paper_id': q.id,
                'subject': q.subject,
            }
            for q in question_papers
        ]
        return JsonResponse({'question_papers': papers_data})

    return render(request, 'student_question_papers.html', {
        'student': student,
        'question_papers': question_papers,
        'available_subjects': available_subjects,
        'selected_semester': semester or '',
        'selected_subject': subject or '',
        'query': query or ''
    })





def custom_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Authenticate user with email and password
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('choose_content')  # Redirect to a dashboard or any other page
        else:
            messages.error(request, "Invalid email or password.")
    
    return render(request, 'login.html')


# Logout view
def user_logout(request):
    logout(request)
    return redirect('login') 

@staff_member_required
def admin_logout(request):
    logout(request)
    return redirect('dashboard')

@login_required
def update_profile(request):
    student = Student.objects.get(user=request.user)
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, instance=student)
        password_form = PasswordChangeForm(request.POST)

        if profile_form.is_valid() and password_form.is_valid():
            old_email = request.user.email
            old_university = student.university  # Assuming the Student model has a 'university' field

            # Save the profile changes
            profile_form.save()
            email = profile_form.cleaned_data.get('email')
            if email:
                request.user.email = email
                request.user.save()

            # Check if the university was updated
            new_university = profile_form.cleaned_data.get('university')
            if new_university != old_university:
                university_updated = True
            else:
                university_updated = False

            # Handle password change
            new_password = password_form.cleaned_data.get('new_password')
            if new_password:
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)  # Keep user logged in

            # ✅ Create profile update notification with specific details
            notification_message = f"{student.user} updated their profile. "
            
            if email != old_email:
                notification_message += f"Email updated from {old_email} to {email}. "
            
            if university_updated:
                notification_message += f"University updated to {new_university}. "
            
            if new_password:
                notification_message += "Password changed."

            # Save the notification with the specific changes
            Notification.objects.create(
                user=request.user,
                message=notification_message.strip(),  # Ensure message is clean of extra spaces
                type='info'
            )

            messages.success(request, 'Your profile has been updated.')
            return redirect('update_profile')

    else:
        profile_form = ProfileUpdateForm(instance=student, initial={'email': request.user.email})
        password_form = PasswordChangeForm()

    return render(request, 'update_profile.html', {
        'profile_form': profile_form,
        'password_form': password_form
    })


