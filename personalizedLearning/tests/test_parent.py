from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_jwt import utils
from personalizedLearning.models import Parent
from personalizedLearning.tests.utils import YGTestUtils

class ParentViewTestCase(TestCase):

    def setUp(self):
        self.yg_util = YGTestUtils()

        self.yg_util.create_superadmin()
        self.yg_util.create_sentinel_student()

        self.client = APIClient()

        datalist = list()
        datalist.append(
            {'username': '余满堂', 'password': '123456', 'email': 'yumantang@yg100.com'})
        datalist.append(
            {'username': '贺阿姨', 'password': '234567', 'email': 'heayi@yg100.com',})
        datalist.append(
            {'username': '许秋平', 'password': '345678', 'email': 'xuqiuping@yg100.com',})
        datalist.append(
            {'username': '马秋林', 'password': '456789', 'email': 'maqiulin@yg100.com',})

        for data in datalist:
            self.response = self.client.post(
                reverse('parent-list'),
                data,
                format='json',
            )

    def test_create_parent(self):

        client = APIClient()

        parent_data = {'username': '刘星星', 'password': '123456', 'email': 'liuxingxing@yg100.com'}
        response = client.post(
            reverse('parent-list'),
            parent_data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_token(self):

        client = APIClient()

        token_data = {'username': '许秋平', 'password': '345678'}
        response = client.post(
            '/api-token-auth/',
            token_data,
            format='json',
        )

        decoded_payload = utils.jwt_decode_handler(response.data['token'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(decoded_payload['username'], token_data['username'])

    def test_get_a_parent(self):

        auth_client = self.yg_util.get_auth_client(username='余满堂', password='123456')

        response = auth_client.get(
            reverse('parent-detail', kwargs={'pk': 1}),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 1)

    def test_update_a_parent_by_self(self):

        auth_client = self.yg_util.get_auth_client(username='贺阿姨', password='234567')

        change_parent = {'username': '余二妈'}
        response = auth_client.put(
            reverse('parent-detail', kwargs={'pk': 2}),
            change_parent, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_a_parent_by_self(self):

        auth_client = self.yg_util.get_auth_client(username='许秋平', password='345678')

        response = auth_client.delete(
            reverse('parent-detail', kwargs={'pk': 3}),
            format='json',
            follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_a_parent_by_admin(self):


        auth_client = self.yg_util.get_auth_client(username='admin', password='password123')

        response = auth_client.delete(
            reverse('parent-detail', kwargs={'pk': 3}),
            format='json',
            follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)