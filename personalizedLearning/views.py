from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets
from personalizedLearning.permissions import UserPermission
from personalizedLearning.models import Student
from personalizedLearning.serializers import StudentSerializer
from personalizedLearning.models import Parent
from personalizedLearning.serializers import ParentSerializer
from personalizedLearning.models import Teacher
from personalizedLearning.serializers import TeacherSerializer
from personalizedLearning.models import CProfile
from personalizedLearning.serializers import CProfileSerializer
from personalizedLearning.models import StudyClass
from personalizedLearning.serializers import StudyClassSerializer
from personalizedLearning.models import Guardianship
from personalizedLearning.serializers import GuardianshipSerializer
from personalizedLearning.models import BaseMessage
from personalizedLearning.serializers import BaseMessageSerializer

# Create your views here.
class StudentViewSet(viewsets.ModelViewSet):

    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class ParentViewSet(viewsets.ModelViewSet):

    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    permission_classes = (UserPermission,)

    def perform_create(self, serializer):
        user = User.objects.create_user(username=self.request.data['username'],
                                        password=self.request.data['password'],
                                        email=self.request.data['email'])
        serializer.save(user=user)

class TeacherViewSet(viewsets.ModelViewSet):

    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = (UserPermission,)

    def perform_create(self, serializer):
        user = User.objects.create_user(username=self.request.data['username'],
                                        password=self.request.data['password'],
                                        email=self.request.data['email'])
        serializer.save(user=user)

class CProfileViewSet(viewsets.ModelViewSet):

    queryset = CProfile.objects.all()
    serializer_class = CProfileSerializer

class StudyClassViewSet(viewsets.ModelViewSet):

    queryset = StudyClass.objects.all()
    serializer_class = StudyClassSerializer

    def perform_create(self, serializer):

        try:
            cprofile_id = self.request.data['cprofile_id']
        except:
            cprofile = CProfile.objects.create(title=self.request.data['title'],
                                                        school=self.request.data['school'])
            cprofile_id = cprofile.id

        # 创建一个缺省的假用户，否则无法创建对应的关系
        try:
            student_id = self.request.data['student_id']
        except:
            student_sentinel = Student.objects.get_or_create(name='sentinel', birth_date='2000-1-1')
            student_id = student_sentinel[0].id

        teacher = Teacher.objects.get(id=self.request.data['teacher_id'])

        serializer.save(student_id = student_id, teacher_id = teacher.id, cprofile_id=cprofile_id)

    def get_queryset(self):

        is_active = self.request.query_params.get('is_active', None)
        cprofile_id = self.request.query_params.get('cprofile_id', None)
        teacher_id = self.request.query_params.get('teacher_id', None)
        student_id = self.request.query_params.get('student_id', None)

        if is_active is not None:
            self.queryset = self.queryset.filter(is_active=is_active)
        if cprofile_id is not None:
            self.queryset = self.queryset.filter(cprofile_id=cprofile_id)
        if teacher_id is not None:
            self.queryset = self.queryset.filter(teacher_id=teacher_id)
        if student_id is not None:
            self.queryset = self.queryset.filter(student_id=student_id)

        return self.queryset

class GuardianViewSet(viewsets.ModelViewSet):

    queryset = Guardianship.objects.all()
    serializer_class = GuardianshipSerializer

    def perform_create(self, serializer):
        # 创建一个缺省的假用户，否则无法创建对应的关系
        try:
            student_id = self.request.data['student_id']
        except:
            student_sentinel = Student.objects.get_or_create(name='sentinel', birth_date='2000-1-1')
            student_id = student_sentinel[0].id

        parent = Parent.objects.get(id=self.request.data['parent_id'])

        serializer.save(student_id = student_id, parent_id = parent.id)

    def get_queryset(self):

        parent_id = self.request.query_params.get('parent_id', None)
        student_id = self.request.query_params.get('student_id', None)

        if parent_id is not None:
            self.queryset = self.queryset.filter(parent_id=parent_id)
        if student_id is not None:
            self.queryset = self.queryset.filter(student_id=student_id)

        return self.queryset

class BaseMessageViewSet(viewsets.ModelViewSet):

    queryset = BaseMessage.objects.all()
    serializer_class = BaseMessageSerializer

    def perform_create(self, serializer):

        teacher = Teacher.objects.get(id=self.request.data['teacher_id'])
        student = Student.objects.get(id=self.request.data['student_id'])

        serializer.save(teacher_id=teacher.id, student_id=student.id)

    def get_queryset(self):
        is_active = self.request.query_params.get('is_active', None)
        teacher_id = self.request.query_params.get('teacher_id', None)
        student_id = self.request.query_params.get('student_id', None)

        if is_active is not None:
            self.queryset = self.queryset.filter(is_active=is_active)
        if teacher_id is not None:
            self.queryset = self.queryset.filter(teacher_id=teacher_id)
        if student_id is not None:
            self.queryset = self.queryset.filter(student_id=student_id)

        return self.queryset