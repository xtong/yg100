from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.test import RequestsClient
from rest_framework import status
from rest_framework_jwt import utils
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# Create your tests here.
from .models import StudyClass
from .models import Teacher
from .models import Student
from .models import Parent
from .models import Guardianship

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

        Student.objects.get_or_create(name='sentinel', birth_date='1975-12-04')

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

class StudyClassTestCase(TestCase):

    def setUp(self):

        self.yg_util = YGTestUtils()
        self.yg_util.create_superadmin()
        self.yg_util.create_sentinel_student()

        self.client = APIClient()

        #创建老师账号
        datalist = list()
        datalist.append({'username': '张翠花', 'password': '123456', 'email': 'zhang@yg100.com', 'subject': Teacher.MATH})
        datalist.append(
            {'username': '田大刀', 'password': '234567', 'email': 'tian@yg100.com', 'subject': Teacher.CHINESE})
        datalist.append(
            {'username': 'Cindy', 'password': '345678', 'email': 'cindy@yg100.com', 'subject': Teacher.ENGLISH})
        datalist.append(
            {'username': 'Betty', 'password': '456789', 'email': 'betty@yg100.com', 'subject': Teacher.ENGLISH})

        for data in datalist:
            self.response = self.client.post(
                reverse('teacher-list'),
                data,
                format='json',
            )

        students = list()
        students.append(
            {'name': '王大锤', 'gender': Student.MALE, 'birth_date': '2008-1-10', 'birth_province': Student.JIANGSU})
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

        study_class_data_list = list()
        study_class_data_list.append({'title': '四年级2班', 'school': '苏杰小学', 'teacher_id': '1'})
        study_class_data_list.append({'title': '四年级3班', 'school': '苏杰小学', 'teacher_id': '1'})

        for data in study_class_data_list:
            self.response = self.client.post(
                reverse('studyclass-list'),
                data,
                format='json'
            )

    def test_create_a_study_class(self):

        client = APIClient()
        study_class_data = {'title': '四年级2班', 'school': '苏杰小学', 'teacher_id': '1'}
        response = client.post(
            reverse('studyclass-list'),
            study_class_data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_new_students(self):

        client = APIClient()

        student_id_list = list()
        # 1 is reserved for sentinel student when initializing a study class
        student_id_list.append({'student_id': '2'})
        student_id_list.append({'student_id': '3'})
        student_id_list.append({'student_id': '4'})
        student_id_list.append({'student_id': '5'})

        query_filter_data = {'school':'苏杰小学', 'title':'四年级2班'}
        response = client.get(
            reverse('studyclass-list'),
            query_filter_data,
            format='json'
        )

        queryset = response.data
        for query in queryset:

            study_class_data = {'teacher_id': query['teacher_id'],
                                'student_id': '1',
                                'title': query['title'],
                                'school': query['school'],
                                'is_active': query['is_active']}
            for student_id in student_id_list:
                study_class_data['student_id'] = student_id['student_id']
                response = client.post(
                    reverse('studyclass-list'),
                    study_class_data,
                    format='json'
                )
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = client.get(
            reverse('studyclass-list'),
            query_filter_data,
            format='json',
        )
        self.assertEqual(len(response.data), 5)

    def test_add_new_teachers(self):

        client = APIClient()

        teacher_id_list = list()
        # 1 is reserved for sentinel student when initializing a study class
        teacher_id_list.append({'teacher_id': '1'})
        teacher_id_list.append({'teacher_id': '2'})
        teacher_id_list.append({'teacher_id': '3'})
        teacher_id_list.append({'teacher_id': '4'})

        query_filter_data = {'school': '苏杰小学', 'title': '四年级2班'}
        response = client.get(
            reverse('studyclass-list'),
            query_filter_data,
            format='json'
        )

        queryset = response.data
        for query in queryset:

            teacher_class_data = {'teacher_id': '1',
                                'student_id': query['student_id'],
                                'title': query['title'],
                                'school': query['school'],
                                'is_active': query['is_active']}
            for teacher_id in teacher_id_list:
                teacher_class_data['teacher_id'] = teacher_id['teacher_id']
                response = client.post(
                    reverse('studyclass-list'),
                    teacher_class_data,
                    format='json'
                )
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = client.get(
            reverse('studyclass-list'),
            query_filter_data,
            format='json',
        )
        self.assertEqual(len(response.data), 5)

    def test_deactivate_study_class(self):

        client = APIClient()
        query_filter_data = {'school': '苏杰小学', 'title': '四年级3班'}
        response = client.get(
            reverse('studyclass-list'),
            query_filter_data,
            format='json',
        )

        queryset = response.data
        deactivation_status = {'is_active': False}
        for query in queryset:
            id = int(query['id'])
            response = client.put(
                reverse('studyclass-detail', kwargs={'pk': id}),
                deactivation_status,
                format='json'
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_a_study_class(self):

        client = APIClient()
        query_filter_data = {'teacher_id': '1'}
        response = client.get(
            reverse('studyclass-list'),
            query_filter_data,
            format='json',
        )

        queryset = response.data
        for query in queryset:
            id = int(query['id'])
            response = client.delete(
                reverse('studyclass-detail', kwargs={'pk': id}),
                format='json',
                follow=True
            )
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)