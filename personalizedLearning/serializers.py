from rest_framework import serializers
from personalizedLearning.models import Parent
from personalizedLearning.models import Student
from personalizedLearning.models import Teacher

class StudentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Student
        fields = ('id', 'name', 'gender', 'birth_date', 'birth_province', 'avatar', 'grade', 'bio')


class ParentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Parent
        fields = ('id', 'name', 'relationship')

class TeacherSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Teacher
        fields = ('id', 'name', 'subject')

class StudyClassSerializer(serializers.HyperlinkedModelSerializer):

    teacher = serializers.HyperlinkedRelatedField(queryset=Teacher.objects.all(), view_name='teacher-detail', many=True)
    student = serializers.HyperlinkedRelatedField(queryset=Student.objects.all(), view_name='student-detail', many=True)

    class Meta:
        model = Student
        fields = ('id', 'title', 'school', 'is_active', 'teacher', 'student')