from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# Create your tests here.
from .models import StudyClass
from .models import Teacher
from .models import Student
from .models import Parent
from .models import Guardianship

class TeacherViewTestCase(TestCase):

    def setUp(self):

        self.client = APIClient()

    def test_create_teacher(self):

        datalist = list()

        datalist.append({'username': '张翠花', 'subject': Teacher.SUBJECT_CHOICES[Teacher.MATH]})
        datalist.append({'username': '田大刀', 'subject': Teacher.SUBJECT_CHOICES[Teacher.CHINESE]})
        datalist.append({'username': 'Cindy', 'subject': Teacher.SUBJECT_CHOICES[Teacher.ENGLISH]})
        datalist.append({'username': 'Betty', 'subject': Teacher.SUBJECT_CHOICES[Teacher.ENGLISH]})

        for data in datalist:
            self.response = self.client.post(
                reverse('teacher-list'),
                data,
                format='json',
            )
            self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
