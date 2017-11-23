from rest_framework import serializers
from personalizedLearning.models import Parent
from personalizedLearning.models import Student
from personalizedLearning.models import Teacher
from personalizedLearning.models import StudyClass
from django.contrib.auth.models import User

class StudentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Student
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source='auth.User')
    # student = StudyClassSerializer(source='studyclass_set', many=True)

    class Meta:
        model = Teacher
        fields = '__all__'

class ParentSerializer(serializers.HyperlinkedModelSerializer):

    username = serializers.ReadOnlyField(source='parent.username')
    class Meta:
        model = Parent
        fields = ('id', 'name', 'relationship')


class StudyClassSerializer(serializers.HyperlinkedModelSerializer):

    teacher_id = serializers.ReadOnlyField(source='teacher.id')
    student_id = serializers.ReadOnlyField(source='student.id')
    # teacher = TeacherSerializer(many=True)
    # student = StudentSerializer(many=True)

    class Meta:
        model = StudyClass
        fields = ('id', 'title', 'school', 'is_active', 'date_created', 'date_modified', 'teacher_id', 'student_id')
        # fields = ('id', 'title', 'school', 'is_active', 'teacher_id', 'student', 'date_created', 'date_modified')


