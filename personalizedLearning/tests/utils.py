from django.contrib.auth.models import User
from rest_framework.test import APIClient
from personalizedLearning.models import Student

class YGTestUtils(object):

    def get_auth_client(self, username, password):

        client = APIClient()

        token_data = {'username': username, 'password': password}
        response = client.post(
            '/api-token-auth/',
            token_data,
            format='json',
        )

        client.credentials(HTTP_AUTHORIZATION='JWT ' + response.data['token'])

        return client

    def create_superadmin(self):

        admin = User.objects.create_superuser(username='admin', password='password123', email='xtong_seu@hotmail.com')

        return admin

    def create_sentinel_student(self):

        Student.objects.get_or_create(name='sentinel', birth_date='2000-1-1')
