from datetime import datetime

from django.db import models
# from django.contrib.auth.models import User
from django.utils.html import escape, mark_safe


class Competition(models.Model):
    id = models.AutoField(primary_key=True, null=False, unique=True, editable=False)
    name = models.CharField(max_length=100, help_text=('Введите название соревнования'))
    desc = models.TextField(help_text=('Введите описание соревнования'), null=False)
    author = models.ForeignKey("User", on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey("Subject", on_delete=models.SET_NULL, null=True)
    state_list = (
        ('w', 'Планируется'),
        ('n', 'Проходит'),
        ('f', 'Завершилось'),
    )
    state = models.CharField(max_length=1, help_text=('Укажите состояние, в котором находится соревнование'),
                             choices=state_list,
                             default='w')
    complexity_list = (
        ('e', 'Легкий'),
        ('n', 'Средний'),
        ('d', 'Сложный'),
    )
    complexity = models.CharField(max_length=1, help_text=('Укажите сложность соревнования'),
                                  choices=complexity_list, default='e')

    date_of_start = models.DateTimeField(default=datetime.now)
    date_of_finish = models.DateTimeField(default=datetime.now)


from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    email = models.EmailField(max_length=254, default='000@rr.ru')


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    competition = models.ManyToManyField(Competition, related_name='competitions')
    groupe = models.CharField(max_length=8, help_text='Укажите номер группы в формате 00-000', null=True)

    institute = (
        ('КФУ', 'Казанский Федеральный Университет'),
        ('ИЭИП', "Институт экологии и природопользования"),
        ('ИГНТ', "Институт геологии и нефтегазовых технологий"),
        ('ИММЛ', "Институт математики и механики им.Н.И.Лобачевского"),
        # "Институт физики",
        # "Химический институт им.А.М.Бутлерова",
        # "Юридический факультет",
        # "Институт вычислительной математики и информационных технологий",
        # "Институт филологии и межкультурной коммуникации",
        # "Институт психологии и образования",
        # "Общеуниверситетская кафедра физического воспитания и спорта",
        # "Институт информационных технологий и интеллектуальных систем",
        # "Институт фундаментальной медицины и биологии",
        # "Инженерный институт",
        # "Институт международных отношений",
        # "Высшая школа бизнеса",
        # "Институт социально-философских наук и массовых коммуникаций",
        # "Институт управления, экономики и финансов",
        # "Высшая школа государственного и муниципального управления",
        # "Центр цифровых трансформаций",
        # "Институт передовых образовательных технологий"
    )
    university_name = models.CharField(max_length=50, choices=institute,
                                       help_text=('Укажите полное название вашего института'), default='КФУ')
    points = models.IntegerField(default=0, editable=False)

    def display_list_competition(self):
        return ', '.join([competition.name for competition in self.competition.all()[:3]])

    display_list_competition.short_description = 'List of Competitions'


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    student_list = models.ManyToManyField(Student, help_text=('Select your students'))
    subject = models.CharField(max_length=70)

    def display_list_students(self):
        return ', '.join([student.user.username for student in self.student_list.all()])

    display_list_students.short_description = 'List of Students'
    institute = (
        ('КФУ', 'Казанский Федеральный Университет'),
        ('ИЭИП', "Институт экологии и природопользования"),
        ('ИГНТ', "Институт геологии и нефтегазовых технологий"),
        ('ИММЛ', "Институт математики и механики им.Н.И.Лобачевского"),
        # "Институт физики",
        # "Химический институт им.А.М.Бутлерова",
        # "Юридический факультет",
        # "Институт вычислительной математики и информационных технологий",
        # "Институт филологии и межкультурной коммуникации",
        # "Институт психологии и образования",
        # "Общеуниверситетская кафедра физического воспитания и спорта",
        # "Институт информационных технологий и интеллектуальных систем",
        # "Институт фундаментальной медицины и биологии",
        # "Инженерный институт",
        # "Институт международных отношений",
        # "Высшая школа бизнеса",
        # "Институт социально-философских наук и массовых коммуникаций",
        # "Институт управления, экономики и финансов",
        # "Высшая школа государственного и муниципального управления",
        # "Центр цифровых трансформаций",
        # "Институт передовых образовательных технологий"
    )
    university_name = models.CharField(max_length=50, choices=institute,
                                       help_text=('Укажите полное название вашего института'), default='КФУ')


class TakenCompetitionn(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='take_competition_student')
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='take_competition_competition')
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)


class Subject(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (color, name)
        return mark_safe(html)


class CompetitionFile(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='competition_with_file')
    test_file = models.FileField(null=True)
    data_file = models.FileField(null=True)
    true_answer_file = models.FileField(null=True)


class AnswerFile(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='user_of_answer')
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='competition_to_answer')
    model_file = models.FileField(null=True)
    data_file = models.FileField(null=True)
    is_public = models.BooleanField(default=True)
    is_copy = models.BooleanField(default=False)

class ColabHref(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='user_colab')
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='competition_colab')
    href = models.CharField(max_length=150)
