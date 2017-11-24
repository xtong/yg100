from rest_framework import serializers
from personalizedLearning.models import Parent
from personalizedLearning.models import Student
from personalizedLearning.models import Teacher
from personalizedLearning.models import StudyClass
from personalizedLearning.models import Guardianship
from django.contrib.auth.models import User

class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source='auth.User')

    class Meta:
        model = Teacher
        fields = '__all__'

class ParentSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source='auth.User')

    class Meta:
        model = Parent
        fields = '__all__'


class StudyClassSerializer(serializers.ModelSerializer):

    teacher_id = serializers.ReadOnlyField(source='teacher.id')
    student_id = serializers.ReadOnlyField(source='student.id')

    class Meta:
        model = StudyClass
        fields = ('id', 'title', 'school', 'is_active', 'teacher_id', 'student_id')

class GuardianshipSerializer(serializers.ModelSerializer):

    parent_id = serializers.ReadOnlyField(source='parent.id')
    student_id = serializers.ReadOnlyField(source='student.id')

    class Meta:
        model = Guardianship
        fields = ('id', 'relationship', 'parent_id', 'student_id')