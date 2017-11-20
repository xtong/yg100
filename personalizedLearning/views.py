from django.shortcuts import render
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from personalizedLearning.models import Student
from personalizedLearning.serializers import StudentSerializer
from personalizedLearning.models import Parent
from personalizedLearning.serializers import ParentSerializer
from personalizedLearning.models import Teacher
from personalizedLearning.serializers import TeacherSerializer
from personalizedLearning.models import StudyClass
from personalizedLearning.serializers import StudyClassSerializer
from personalizedLearning.permissions import IsParentOrReadOnly

# Create your views here.
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class ParentViewSet(viewsets.ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class StudyClassViewSet(viewsets.ModelViewSet):
    queryset = StudyClass.objects.all()
    serializer_class = StudyClassSerializer