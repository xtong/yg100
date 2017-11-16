from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ChildProfile(models.Model):
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

    # user = models.OneToOneField(User, unique=True, db_index=True, related_name='childProfile')

    name = models.CharField(blank=True, max_length=255, db_index=True)
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, default=FEMALE)
    birth_date = models.DateField(null=False, blank=False)
    birth_province = models.SmallIntegerField(choices=PROVINCE_CHOICES, default=BEIJING)

    avatar = models.URLField(blank=True, max_length=255, default='')
    grade = models.SmallIntegerField(null=False, blank=True) # from primary school till high school: 1 ~ 12
    bio = models.TextField(null=True, blank=True, max_length=140) # self-introduction

    class Meta:
        db_table = 'auth_childProfile'

    def __unicode__(self):
        return self.name

class ParentProfile(models.Model):
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
        (GUARDIAN, '家长'), # 其他监护人
    )
    user = models.OneToOneField(User, unique=True, db_index=True, related_name='parentProfile')

    name = models.CharField(blank=True, max_length=255, db_index=True)

    relationship = models.SmallIntegerField(choices=RELATIONSHIP_CHOICES, default=MATHER)

    class Meta:
        db_table = 'auth_parentProfile'

    def __unicode__(self):
        return self.name

class TeacherProfile(models.Model):
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
    user = models.OneToOneField(User, unique=True, db_index=True, related_name='teacherProfile')

    name = models.CharField(blank=True, max_length=255, db_index=True)

    subject = models.SmallIntegerField(choices=SUBJECT_CHOICES, default=MATH)

    class Meta:
        db_table = 'auth_teacherProfile'

    def __unicode__(self):
        return self.name