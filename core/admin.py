from django.contrib import admin
from .models import University, Course, StudyMaterial, Student , QuestionPaper

def get_all_field_names(model):
    return [field.name for field in model._meta.fields]

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = get_all_field_names(University)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = get_all_field_names(Course)

@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = get_all_field_names(StudyMaterial)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = get_all_field_names(Student)


@admin.register(QuestionPaper)
class StudentAdmin(admin.ModelAdmin):
    list_display = get_all_field_names(QuestionPaper)