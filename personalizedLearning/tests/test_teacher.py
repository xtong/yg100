from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_jwt import utils
from personalizedLearning.models import Teacher
from personalizedLearning.tests.utils import YGTestUtils

class TeacherViewTestCase(TestCase):

    def setUp(self):

        self.yg_util = YGTestUtils()

        self.yg_util.create_superadmin()
        self.yg_util.create_sentinel_student()

        self.client = APIClient()

        datalist = list()
        datalist.append({'username': '张翠花', 'password': '123456', 'email': 'zhang@yg100.com', 'subject': Teacher.MATH})
        datalist.append({'username': '田大刀', 'password': '234567', 'email': 'tian@yg100.com', 'subject': Teacher.CHINESE})
        datalist.append({'username': 'Cindy', 'password': '345678', 'email': 'cindy@yg100.com', 'subject': Teacher.ENGLISH})
        datalist.append({'username': 'Betty', 'password': '456789', 'email': 'betty@yg100.com', 'subject': Teacher.ENGLISH})

        for data in datalist:
            self.response = self.client.post(
                reverse('teacher-list'),
                data,
                format='json',
            )

    def test_get_token(self):

        client = APIClient()

        token_data = {'username': 'Cindy', 'password': '345678'}
        response = client.post(
            '/api-token-auth/',
            token_data,
            format='json',
        )

        decoded_payload = utils.jwt_decode_handler(response.data['token'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(decoded_payload['username'], token_data['username'])

    def test_create_teacher(self):

        teacher_data = {'username': 'Jane', 'password': '123456', 'email': 'jane@yg100.com', 'subject': Teacher.ENGLISH}

        self.response = self.client.post(
            reverse('teacher-list'),
            teacher_data,
            format='json',
        )
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_get_a_teacher(self):

        auth_client = self.yg_util.get_auth_client(username='张翠花', password='123456')

        response = auth_client.get(
            reverse('teacher-detail',  kwargs={'pk': 1}),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 1)

    def test_update_a_teacher_by_self(self):

        auth_client = self.yg_util.get_auth_client(username='田大刀', password='234567')

        change_teacher = {'username': '老田'}
        response = auth_client.put(
            reverse('teacher-detail', kwargs={'pk': 2}),
            change_teacher, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_a_teacher_by_self(self):

        auth_client = self.yg_util.get_auth_client(username='Cindy', password='345678')

        response = auth_client.delete(
            reverse('teacher-detail', kwargs={'pk': 3}),
            format='json',
            follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_a_teacher_by_admin(self):

        auth_client = self.yg_util.get_auth_client(username='admin', password='password123')

        response = auth_client.delete(
            reverse('teacher-detail', kwargs={'pk': 3}),
            format='json',
            follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)