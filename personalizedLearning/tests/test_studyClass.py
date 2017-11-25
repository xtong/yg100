from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework.test import APIClient
from rest_framework import status
from personalizedLearning.models import Teacher
from personalizedLearning.models import Student
from personalizedLearning.tests.utils import YGTestUtils

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
        study_class_data_list.append({'title': '四年级2班', 'school': '苏杰小学', 'teacher_id': '1'}) # id == 1
        study_class_data_list.append({'title': '四年级3班', 'school': '苏杰小学', 'teacher_id': '2'}) # id == 2

        for data in study_class_data_list:
            self.response = self.client.post(
                reverse('studyclass-list'),
                data,
                format='json'
            )

    def test_create_a_study_class(self):

        client = APIClient()
        study_class_data = {'title': '四年级2班', 'school': '苏杰小学', 'teacher_id': '3'}
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

        query_filter_data = {'cprofile_id': '1'}
        response = client.get(
            reverse('studyclass-list'),
            query_filter_data,
            format='json'
        )

        queryset = response.data
        for query in queryset:

            study_class_data = {'teacher_id': query['teacher_id'],
                                'student_id': query['student_id'],
                                'cprofile_id': query['cprofile_id'],
                                'is_active': query['is_active']}
            for student_id in student_id_list:
                if str(query['student_id']) == str(student_id['student_id']):
                    continue
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
        # 去除重复的老师, 需要在前端或SDK中去重
        teacher_id_list.append({'teacher_id': '1'})
        teacher_id_list.append({'teacher_id': '2'})
        teacher_id_list.append({'teacher_id': '3'})
        teacher_id_list.append({'teacher_id': '4'})

        query_filter_data = {'cprofile_id': '2'}
        response = client.get(
            reverse('studyclass-list'),
            query_filter_data,
            format='json'
        )

        queryset = response.data
        for query in queryset:
            teacher_class_data = {'teacher_id': query['teacher_id'],
                                'student_id': query['student_id'],
                                'cprofile_id': query['cprofile_id'],
                                'is_active': query['is_active']}
            for teacher_id in teacher_id_list:

                if str(query['teacher_id']) == str(teacher_id['teacher_id']):
                    continue

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
        self.assertEqual(len(response.data), 4)

    def test_deactivate_study_class(self):

        client = APIClient()
        query_filter_data = {'class_id': '2'}
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
        query_filter_data = {'class_id': '1'}
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