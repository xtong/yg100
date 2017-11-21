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

        datalist = list()
        datalist.append({'username': '张翠花', 'password': '123456', 'subject': Teacher.MATH})
        datalist.append({'username': '田大刀', 'password': '234567', 'subject': Teacher.CHINESE})
        datalist.append({'username': 'Cindy', 'password': '345678', 'subject': Teacher.ENGLISH})
        datalist.append({'username': 'Betty', 'password': '456789', 'subject': Teacher.ENGLISH})

        for data in datalist:
            self.response = self.client.post(
                reverse('teacher-list'),
                data,
                format='json',
            )
            self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_get_token(self):

        teacher_data = {'username': 'Jane', 'password': '123456', 'subject': Teacher.ENGLISH}

        self.response = self.client.post(
            reverse('teacher-list'),
            teacher_data,
            format='json',
        )
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        token_data = {'username': 'Jane', 'password': '123456'}
        self.response = self.client.post(
            '/api-token-auth/',
            token_data,
            format='json',
        )
        print(token_data)
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_create_teacher(self):

        teacher_data = {'username': 'Jane', 'password': '123456', 'subject': Teacher.ENGLISH}

        self.response = self.client.post(
            reverse('teacher-list'),
            teacher_data,
            format='json',
        )
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_get_a_teacher(self):

        teacher = Teacher.objects.get(id=1)
        response = self.client.get(
            '/teacher/',
            kwargs={'pk': teacher.id}, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, teacher.id)

    def test_update_a_teacher(self):

        teacher = Teacher.objects.get(id=2)
        change_teacher = {'username': '李茉莉'}
        response = self.client.put(
            reverse('teacher-detail', kwargs={'pk': teacher.id}),
            change_teacher, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_a_teacher(self):

        teacher = Teacher.objects.get(id=3)
        response = self.client.delete(
            reverse('teacher-detail', kwargs={'pk': teacher.id}),
            format='json',
            follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)