from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework.test import APIClient
from rest_framework import status
from personalizedLearning.models import Student
from personalizedLearning.tests.utils import YGTestUtils

class StudentTestCase(TestCase):

    def setUp(self):

        self.yg_util = YGTestUtils()
        self.yg_util.create_superadmin()
        self.yg_util.create_sentinel_student()

        self.client = APIClient()

        students = list()
        students.append({'name': '王大锤', 'gender': Student.MALE, 'birth_date': '2008-1-10', 'birth_province': Student.JIANGSU})
        students.append(
            {'name': '安嘉璐', 'gender': Student.FEMALE, 'birth_date': '2008-11-30', 'birth_province': Student.JIANGSU})
        students.append(
            {'name': '余小二', 'gender': Student.MALE, 'birth_date': '2008-10-10', 'birth_province': Student.SHANX})
        students.append(
            {'name': '周文涓', 'gender': Student.FEMALE, 'birth_date': '2008-11-10', 'birth_province': Student.BEIJING})

        for student in students:
            response = self.client.post(
                reverse('student-list'),
                student,
                format='json'
            )

    def test_create_student(self):

        client = APIClient()
        student = {'name': '李二冬', 'gender': Student.MALE, 'birth_date': '2008-3-10', 'birth_province': Student.JIANGSU}
        response = client.post(
            reverse('student-list'),
            student,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_a_student(self):

        client = APIClient()
        response = client.get(
            reverse('student-detail', kwargs={'pk': 4}),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, '余小二')

    def test_update_a_student(self):

        client = APIClient()
        new_student = {'name': '大胸姐', 'birth_date': '2007-11-30'}
        response = client.put(
            reverse('student-detail', kwargs={'pk': 3}),
            new_student, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_a_student(self):

        client = APIClient()
        response = client.delete(
            reverse('student-detail', kwargs={'pk': 4}),
            format='json',
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)