from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework.test import APIClient
from rest_framework import status
from personalizedLearning.models import Parent
from personalizedLearning.models import Student
from personalizedLearning.models import Guardianship
from personalizedLearning.tests.utils import YGTestUtils

class GuardianTestCase(TestCase):

    def setUp(self):

        self.yg_util = YGTestUtils()
        self.yg_util.create_superadmin()
        self.yg_util.create_sentinel_student()

        self.client = APIClient()

        #创建老师账号
        datalist = list()
        datalist.append(
            {'username': '余满堂', 'password': '123456', 'email': 'yumantang@yg100.com'})
        datalist.append(
            {'username': '贺阿姨', 'password': '234567', 'email': 'heayi@yg100.com', })
        datalist.append(
            {'username': '许秋平', 'password': '345678', 'email': 'xuqiuping@yg100.com', })
        datalist.append(
            {'username': '马秋林', 'password': '456789', 'email': 'maqiulin@yg100.com', })

        for data in datalist:
            self.response = self.client.post(
                reverse('parent-list'),
                data,
                format='json',
            )

        students = list()
        students.append(
            {'name': '王大锤', 'gender': Student.MALE, 'birth_date': '2008-1-10', 'birth_province': Student.JIANGSU})
        # students.append(
        #     {'name': '安嘉璐', 'gender': Student.FEMALE, 'birth_date': '2008-11-30', 'birth_province': Student.JIANGSU})
        # students.append(
        #     {'name': '余小二', 'gender': Student.MALE, 'birth_date': '2008-10-10', 'birth_province': Student.SHANX})
        # students.append(
        #     {'name': '周文涓', 'gender': Student.FEMALE, 'birth_date': '2008-11-10', 'birth_province': Student.BEIJING})

        for student in students:
            response = self.client.post(
                reverse('student-list'),
                student,
                format='json'
            )

        guardianship_data_list = list()
        guardianship_data_list.append({'relationship': Guardianship.FATHER, 'parent_id': '1', 'student_id': '2'})
        guardianship_data_list.append({'relationship': Guardianship.MATHER, 'parent_id': '2', 'student_id': '2'})

        for data in guardianship_data_list:
            self.response = self.client.post(
                reverse('guardianship-list'),
                data,
                format='json'
            )

    def test_create_a_guardianship(self):

        client = APIClient()
        guardianship_data = {'relationship': Guardianship.FATHER, 'parent_id': '3'}
        response = client.post(
            reverse('guardianship-list'),
            guardianship_data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

