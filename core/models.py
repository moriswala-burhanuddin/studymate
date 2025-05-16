from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone  

class University(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class YearSemester(models.Model):
    name = models.CharField(max_length=100)  # e.g., "Year 1", "Semester 2"

    def __str__(self):
        return self.name

class StudyMaterial(models.Model):
    title = models.CharField(max_length=255)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    year_or_semester = models.ForeignKey(YearSemester, on_delete=models.CASCADE)
    semester = models.CharField(max_length=10, blank=True)
    subject = models.CharField(max_length=255, blank=True)
    file_upload = models.FileField(upload_to='materials/', blank=True, null=True)
    drive_link = models.URLField(blank=True)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to Django's built-in User model
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    year_or_semester = models.ForeignKey(YearSemester, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    # Any additional fields like address, profile picture, etc.
    registration_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username


class QuestionPaper(models.Model):
    title = models.CharField(max_length=255)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    year_or_semester = models.ForeignKey(YearSemester, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255, blank=True)
    file_upload = models.FileField(upload_to='question_papers/', blank=True, null=True)
    drive_link = models.URLField(blank=True)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    semester = models.CharField(max_length=10, blank=True)
    def __str__(self):
        return self.title

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', null=True)  # temporarily allow nulls
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20, default='info')

    def __str__(self):
        return f"{self.user} - {self.message[:20]}"
