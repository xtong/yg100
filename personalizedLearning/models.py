from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Parent(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # name = models.CharField(blank=True, max_length=255)

    class Meta:
        db_table = 'parent'

    def __str__(self):
        return self.user.username

class Student(models.Model):
    # 出生地（省）列表
    BEIJING = 1
    TIANJIN = 2
    SHANGHAI = 3
    CHONGQING = 4
    HEBEI = 5
    HENAN = 6
    YUNNAN = 7
    LIAONING = 8
    HEILONGJIANG = 9
    HUNAN = 10
    ANHUI = 11
    SHANDONG = 12
    XINJIANG = 13
    JIANGSU = 14
    HUBEI = 15
    GUANGXI = 16
    GANSU = 17
    SHANXI = 18
    NEIMENG = 19
    SHANX = 20
    JILIN = 21
    FUJIAN = 22
    GUIZHOU = 23
    GUANGDONG = 24
    QINGHAI = 25
    TIBET = 26
    NINGXIA = 27
    HAINAN = 28
    TAIWAN = 29
    HANGKONG = 30
    MACAO = 31
    PROVINCE_CHOICES = (
        (BEIJING, '北京'),
        (TIANJIN, '天津'),
        (SHANGHAI, '上海'),
        (CHONGQING, '重庆'),
        (HEBEI, '河北'),
        (HENAN, '河南'),
        (YUNNAN, '云南'),
        (LIAONING, '辽宁'),
        (HEILONGJIANG, '黑龙江'),
        (HUNAN, '湖南'),
        (ANHUI, '安徽'),
        (SHANDONG, '山东'),
        (XINJIANG, '新疆'),
        (JIANGSU, '江苏'),
        (HUBEI, '河北'),
        (GUANGXI, '广西'),
        (GANSU, '甘肃'),
        (SHANXI, '山西'),
        (NEIMENG, '内蒙古'),
        (SHANX, '陕西'),
        (JILIN, '吉林'),
        (FUJIAN, '福建'),
        (GUIZHOU, '贵州'),
        (GUANGDONG, '广东'),
        (QINGHAI, '青海'),
        (TIBET, '西藏'),
        (NINGXIA, '宁夏'),
        (HAINAN, '海南'),
        (TAIWAN, '台湾'),
        (HANGKONG, '香港'),
        (MACAO, '澳门'),
    )

    MALE = 1
    FEMALE = 2
    GENDER_CHOICES = (
        (MALE, '男'),
        (FEMALE, '女'),
    )

    name = models.CharField(blank=False, max_length=255)
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, default=FEMALE)
    birth_date = models.DateField(blank=False)
    birth_province = models.SmallIntegerField(choices=PROVINCE_CHOICES, default=BEIJING)

    avatar = models.URLField(blank=True, max_length=255, default='')

    GRADE_1 = 1
    GRADE_2 = 2
    GRADE_3 = 3
    GRADE_4 = 4
    GRADE_5 = 5
    GRADE_6 = 6
    GRADE_7 = 7
    GRADE_8 = 8
    GRADE_9 = 9
    GRADE_10 = 10
    GRADE_11 = 11
    GRADE_12 = 12
    GRADE_CHOICES = (
        (GRADE_1, '一年级'),
        (GRADE_2, '二年级'),
        (GRADE_3, '三年级'),
        (GRADE_4, '四年级'),
        (GRADE_5, '五年级'),
        (GRADE_6, '六年级'),
        (GRADE_7, '初中一年级'),
        (GRADE_8, '初中二年级'),
        (GRADE_9, '初中三年级'),
        (GRADE_10, '高中一年级'),
        (GRADE_11, '高中二年级'),
        (GRADE_12, '高中三年级'),
    )
    grade = models.SmallIntegerField(choices=GRADE_CHOICES, default=GRADE_4) # from primary school till high school: 1 ~ 12
    bio = models.TextField(blank=True, max_length=140) # self-introduction

    parent = models.ManyToManyField(Parent, through='Guardianship')

    class Meta:
        db_table = 'student'

    def __str__(self):
        return self.name

class Teacher(models.Model):
    CHINESE = 1
    MATH = 2
    ENGLISH = 3
    BIOLOGY = 4
    PHYSICS = 5
    CHEMISTRY = 6
    HISTORY = 7
    GEOGRAPHY = 8
    POLITICS = 9
    SUBJECT_CHOICES = (
        (CHINESE, '语文'),
        (MATH, '数学'),
        (ENGLISH, '英语'),
        (BIOLOGY, '生物'),
        (PHYSICS, '物理'),
        (CHEMISTRY, '化学'),
        (HISTORY, '历史'),
        (GEOGRAPHY, '地理'),
        (POLITICS, '政治'),
    )
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    student = models.ManyToManyField('Student', through='StudyClass')

    subject = models.SmallIntegerField(choices=SUBJECT_CHOICES, default=MATH)

    class Meta:
        db_table = 'teacher'

    def __str__(self):
        return self.user.username

class StudyClass(models.Model):
    title = models.CharField(blank=True, max_length=64)
    school = models.CharField(blank=True, max_length=128)
    is_active = models.BooleanField(default=True)

    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)

    class Meta:
        db_table = 'study_class'

    def __str__(self):
        return self.title

class Guardianship(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)

    FATHER = 1
    MATHER = 2
    GRANDPA = 3
    GRANDMA = 4
    GUARDIAN = 5
    RELATIONSHIP_CHOICES = (
        (FATHER, '爸爸'),
        (MATHER, '妈妈'),
        (GRANDPA, '爷爷'),
        (GRANDMA, '奶奶'),
        (GUARDIAN, '家长'),  # 其他监护人
    )

    relationship = models.SmallIntegerField(choices=RELATIONSHIP_CHOICES, default=MATHER)

    class Meta:
        db_table = 'guardianship'

    def __str__(self):
        return self.student.objects.all() + '和' + self.parent.objects.all() + '的家'