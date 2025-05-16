from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    university = serializers.CharField(source='university.name')
    course = serializers.CharField(source='course.name')
    year_or_semester = serializers.CharField(source='year_or_semester.name')

    class Meta:
        model = Student
        fields = ['id', 'username', 'university', 'course', 'year_or_semester', 'phone', 'registration_date']
