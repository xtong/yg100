from django.shortcuts import render
from rest_framework import permissions
from rest_framework import viewsets
from personalizedLearning.models import ChildProfile
from personalizedLearning.serializers import ChildSerializer
from personalizedLearning.models import ParentProfile
from personalizedLearning.serializers import ParentSerializer
from personalizedLearning.models import TeacherProfile
from personalizedLearning.serializers import TeacherSerializer

# Create your views here.
class ChildViewSet(viewsets.ModelViewSet):
    queryset = ChildProfile.objects.all()
    serializer_class = ChildSerializer
    permission_classes = (permissions.IsAuthenticated,)

class ParentViewSet(viewsets.ModelViewSet):
    queryset = ParentProfile.objects.all()
    serializer_class = ParentSerializer
    permission_classes = (permissions.IsAuthenticated,)

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = (permissions.IsAuthenticated,)
