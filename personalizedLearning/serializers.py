from rest_framework import serializers
from personalizedLearning.models import ParentProfile
from personalizedLearning.models import ChildProfile
from personalizedLearning.models import TeacherProfile

class ChildSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChildProfile
        fields = ('id', 'name', 'gender', 'birth_date', 'birth_province', 'avatar', 'grade', 'bio')


class ParentSerializer(serializers.ModelSerializer):
    children = ChildSerializer(many=True)

    class Meta:
        model = ParentProfile
        fields = ('id', 'name', 'relationship', 'children')

class TeacherSerializer(serializers.ModelSerializer):
    children = ChildSerializer(many=True)

    class Meta:
        model = TeacherProfile
        fields = ('id', 'name', 'subject', 'children')