from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import list_route
from personalizedLearning.permissions import UserPermission
from personalizedLearning.models import Student
from personalizedLearning.serializers import StudentSerializer
from personalizedLearning.models import Parent
from personalizedLearning.serializers import ParentSerializer
from personalizedLearning.models import Teacher
from personalizedLearning.serializers import TeacherSerializer
from personalizedLearning.models import StudyClass
from personalizedLearning.serializers import StudyClassSerializer

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
    permission_classes = (UserPermission,)

    def perform_create(self, serializer):
        user = User.objects.create(username=self.request.data['username'])
        serializer.save(user=user)

class StudyClassViewSet(viewsets.ModelViewSet):
    queryset = StudyClass.objects.all()
    serializer_class = StudyClassSerializer