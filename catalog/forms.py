from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from catalog.models import (Student, User, Teacher, CompetitionFile, AnswerFile, Competition, ColabHref, Subject)

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
state_list = (
    ('w', 'Планируется'),
    ('n', 'Проходит'),
    ('f', 'Завершилось'),
)
complexity_list = (
    ('e', 'Легкий'),
    ('n', 'Средний'),
    ('d', 'Сложный'),
)
subject = (
    ()
)


class StudentSignUpForm(UserCreationForm):
    password = forms.CharField(widget=forms.PasswordInput())
    university = forms.ChoiceField(
        choices=institute,
        widget=forms.Select,
        required=True,
        label='Выберите свой институт'
    )
    email = forms.EmailField(
        required=True
    )
    groupe = forms.CharField(
        label='Укажите вашу группу в формате 00-000',
        required=True,
        widget=forms.TextInput,
    )
    name = forms.CharField(
        label='Укажите ваше настоящее имя',
        required=True,
        widget=forms.TextInput,
    )
    surname = forms.CharField(
        label='Укажите вашу настоящую имя',
        required=True,
        widget=forms.TextInput,
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.email = self.cleaned_data.get('email')
        user.save()
        student = Student.objects.create(user=user)
        student.university_name = self.cleaned_data.get('university')
        return user


class TeacherSignUpForm(UserCreationForm):
    university = forms.ChoiceField(
        choices=institute,
        widget=forms.Select,
        required=True,
        label='Выберите свой институт'
    )
    email = forms.EmailField(
        required=True
    )
    subject = forms.CharField(
        widget=forms.TextInput,
        label="Укажите вашу специальность",
        required=False
    )

    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.email = self.cleaned_data.get('email')
            user.save()
            teacher = Teacher.objects.create(user=user)
            teacher.university_name = self.cleaned_data.get('university')
            teacher.subject = self.cleaned_data.get('subject')
        return user


class DownCompFileForm(forms.ModelForm):
    class Meta:
        model = CompetitionFile
        fields = ['competition', 'test_file', 'data_file']


class ColabHrefForm(forms.ModelForm):
    href = forms.CharField(
        widget=forms.TextInput,
        required=True
    )

    class Meta:
        model = ColabHref
        fields = ['href', ]


class DownAnswerFileForm(forms.ModelForm):
    class Meta:
        model = AnswerFile
        fields = ['competition', 'model_file', 'data_file', 'is_public']


def subjecthelp():
    subset = Subject.objects.all()
    subsname = list()
    innerlist = list()
    for sub in subset:
        innerlist.extend([sub.name])
        innerlist.extend([sub.name])
        innerlist = tuple(innerlist)
        subsname.extend([innerlist])
        innerlist = list()
    subsname = tuple(subsname)
    return subsname


class AddNewCompetitionForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput,
        required=True,
        label='Укажите название'
    )
    desc = forms.CharField(
        widget=forms.Textarea,
        required=True,
        label='Добавьте описание'
    )
    state = forms.ChoiceField(
        choices=state_list,
        widget=forms.Select,
        label="Укажите состояние вашего соревнования",
        required=True
    )
    complexity = forms.ChoiceField(
        choices=complexity_list,
        widget=forms.Select,
        label="Укажите сложность вашего соревнования",
        required=True
    )
    subject = forms.ChoiceField(
        label="Укажите тип задачи",
        choices=subjecthelp()
    )
    date_of_start = forms.DateField(
        label="Дата старта",
        widget=forms.DateInput
    )
    date_of_finish = forms.DateField(
        label="Дата окончания",
        widget=forms.DateInput
    )

    class Meta():
        model = Competition
        fields = ('name', 'desc', 'subject', 'state', 'complexity', 'date_of_start', 'date_of_finish')


class AddCompetitionFileForm(forms.ModelForm):
    class Meta:
        model = CompetitionFile
        fields = ['competition', 'test_file', 'data_file', 'true_answer_file']
