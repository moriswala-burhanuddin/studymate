from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_redirect_view, name='home'),
    path('admin-panel/', views.dashboard, name='dashboard'),
    path('upload/', views.upload_material, name='upload'),
    path('edit/<int:pk>/', views.edit_material, name='edit'),
    path('delete/<int:pk>/', views.delete_material, name='delete'),
    path('add-university/', views.add_university, name='add_university'),
    path('add-course/', views.add_course, name='add_course'),
    path('add-year/', views.add_yearsemester, name='add_yearsemester'),
    path('student-signup/', views.student_signup, name='student_signup'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('edit-student/<int:student_id>/', views.edit_student, name='edit_student'),
    path('delete-student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('add-student/', views.add_student, name='add_student'),
    path('choose-content/', views.choose_content, name='choose_content'),
    # urls.py
    path('materials/', views.student_materials, name='student_materials'),

    path('questions/', views.student_question_papers, name='student_question_papers'),

    path('upload_question_paper/', views.upload_question_paper, name='upload_question_paper'),
   path('edit_question_paper/<int:pk>/', views.edit_question_paper, name='edit_question_paper'),
    path('delete_question_paper/<int:pk>/', views.delete_question_paper, name='delete_question_paper'),
   
    path('admin-logout/', views.admin_logout, name='admin_logout'),
 
]
