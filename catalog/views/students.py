import os

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import smart_str
from django.views.generic import CreateView, ListView, UpdateView

from ..decorators import student_required
from ..forms import StudentSignUpForm, DownAnswerFileForm, ColabHrefForm
from catalog.models import Student, User, Competition, TakenCompetitionn, \
    AnswerFile, CompetitionFile, ColabHref, Subject
from ..check_answer import binary_class


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


@method_decorator([login_required, student_required], name='dispatch')
class CompetitionView(ListView):
    model = Competition
    ordering = ('date_of_start',)
    context_object_name = 'competitions'
    template_name = './students/competition_list.html'

    def get_queryset(self):
        queryset = Competition.objects.all().select_related('subject')
        return queryset


@method_decorator([login_required, student_required], name='dispatch')
class TakenCompetitionListView(ListView):
    model = TakenCompetitionn
    context_object_name = 'taken_competitions'
    template_name = './students/taken_competition_list.html'

    def get_queryset(self):
        queryset = self.request.user.student.take_competition_student \
            .select_related('competition', 'competition__subject') \
            .order_by('competition__date_of_finish')
        return queryset


@login_required
def model_form_upload(request, pk):
    competition = get_object_or_404(Competition, pk=pk)
    student = request.user.student

    if request.method == 'POST':
        my_model = 0
        try:
            my_model = AnswerFile.objects.get(student=student, competition=competition)
        except:
            print("нет")
        # if my_model != 0:
        #     return redirect('students:take_competition')
        my_href = 0
        try:
            my_href = ColabHref.objects.get(student=student, competition=competition)
        except:
            print("нет!")

        if my_href != 0 and my_model != 0:
            return redirect('students:take_competition')
        my_href = 0
        try:
            my_href = request.POST['href']
        except:
            print('yyyyyy')
        if my_href != 0:
            ColabHref.objects.create(student_id=request.user.id, competition_id=competition.id,
                                     href=my_href)
            return render(request, './students/add_answer_file.html', {
                'form': DownAnswerFileForm(),
                'form1': ColabHrefForm(),
            })
        else:
            try:
                a = request.POST['is_public']
                is_public = True
            except:
                is_public = False

            user_answer_file_name = AnswerFile.objects.create(student_id=request.user.id,
                                                              competition_id=competition.id,
                                                              model_file=request.FILES['model_file'],
                                                              data_file=request.FILES['data_file'],
                                                              is_public=is_public).data_file
            true_answer_file_name = get_object_or_404(CompetitionFile, competition=competition).true_answer_file
            points = binary_class(true_answer_file_name, user_answer_file_name)
            TakenCompetitionn.objects.filter(student=student, competition=competition).update(score=points)
            Student.objects.filter(user_id=request.user.id).update(points=student.points + points)
            return redirect('students:take_competition')
    else:
        return render(request, './students/add_answer_file.html', {
            'form': DownAnswerFileForm(),
            'form1': ColabHrefForm(),
        })


@method_decorator([login_required, student_required], name='dispatch')
class PersonalAccountView(ListView):  # новый
    model = Student
    context_object_name = 'user_data'
    template_name = './students/personal_account.html'

    def get_queryset(self):
        # queryset = self.request.user.student.take_competition_student \
        #     .select_related('competition', 'competition__subject') \
        #     .order_by('competition__date_of_finish')
        # queryset = self.request.user.take_competition_student.select_related('competition', 'student')
        queryset = Student.objects.select_related('user').get(user=self.request.user)
        p = Student.objects.select_related('user').get(user=self.request.user)
        print(p.user.first_name)
        return queryset


@login_required
def add_new_comp(request, pk):
    competition = get_object_or_404(Competition, pk=pk)
    student = request.user.student
    maybeComp = 0
    try:
        maybeComp = TakenCompetitionn.objects.get(student=student, competition=competition)
    except:
        print("maybeComp not")
    if maybeComp == 0:
        TakenCompetitionn.objects.create(student=student, competition_id=competition.id, score=0)
    return redirect('students:take_competition')


@login_required
def download_competition_test_data(request, pk):
    comp = CompetitionFile.objects.get(competition_id=pk)
    path_to_file = comp.test_file.path
    filename = os.path.basename(path_to_file)
    response = HttpResponse(comp.data_file, content_type='application/msword')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(filename)
    response['X-Sendfile'] = smart_str(path_to_file)
    return response


@login_required
def download_competition_study_data(request, pk):
    comp = CompetitionFile.objects.get(competition_id=pk)
    path_to_file = comp.data_file.path
    filename = os.path.basename(path_to_file)
    response = HttpResponse(comp.data_file, content_type='application/msword')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(filename)
    response['X-Sendfile'] = smart_str(path_to_file)
    return response


@login_required
def download_answer_model(request, pk):
    comp = get_object_or_404(AnswerFile, competition_id=pk)
    path_to_file = comp.data_file.path
    filename = os.path.basename(path_to_file)
    response = HttpResponse(comp.data_file, content_type='multipart/form-data')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(filename)
    response['X-Sendfile'] = smart_str(path_to_file)
    return response


@login_required
def download_answer_data(request, pk):
    comp = AnswerFile.objects.get(competition_id=pk)
    path_to_file = comp.data_file.path
    filename = os.path.basename(path_to_file)
    response = HttpResponse(comp.data_file, content_type='multipart/form-data')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(filename)
    response['X-Sendfile'] = smart_str(path_to_file)
    return response


@student_required
def one_competition(request, pk):
    competition = get_object_or_404(Competition, pk=pk)
    student = request.user.student

    maybeColabHref = 0
    try:
        maybeColabHref = ColabHref.objects.get(student=student, competition=competition)
    except:
        print("maybeComp not")

    answerFiles = 0
    try:
        answerFiles = AnswerFile.objects.get(student=student, competition=competition)
    except:
        print("answerFiles not")

    competitionfile = 0
    try:
        competitionfile = CompetitionFile.objects.get(competition=competition)
    except:
        print("competitionfile not")

    otherAnswerFiles = 0
    try:
        otherAnswerFiles = AnswerFile.objects.exclude(student=student).filter(competition=competition,
                                                                              is_public=True).select_related('student',
                                                                                                             'student__user')
    except:
        print('otherAnswerFiles not')

    subject = competition.subject.name
    author = competition.author.username
    if maybeColabHref != 0:
        if answerFiles != 0:
            return render(request, './students/one_comp.html', {
                'author': author,
                'subject': subject,
                'competition': competition,
                'colabHref': maybeColabHref,
                'answerFiles': answerFiles,
                'competitionfile': competitionfile,
                'otherAnswerFiles': otherAnswerFiles
            })
        else:
            return render(request, './students/one_comp.html', {
                'author': author,
                'subject': subject,
                'competition': competition,
                'colabHref': maybeColabHref,
                'competitionfile': competitionfile,
                'otherAnswerFiles': otherAnswerFiles
            })
    else:
        if answerFiles != 0:
            return render(request, './students/one_comp.html', {
                'author': author,
                'subject': subject,
                'competition': competition,
                'answerFiles': answerFiles,
                'competitionfile': competitionfile,
                'otherAnswerFiles': otherAnswerFiles
            })
        else:
            return render(request, './students/one_comp.html', {
                'author': author,
                'subject': subject,
                'competition': competition,
                'competitionfile': competitionfile,
                'otherAnswerFiles': otherAnswerFiles
            })
