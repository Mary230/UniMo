from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from ..forms import TeacherSignUpForm, AddNewCompetitionForm, AddCompetitionFileForm
from ..models import User, Competition, ColabHref, AnswerFile, CompetitionFile, Subject, Teacher, TakenCompetitionn
from ..decorators import teacher_required
from django.views.generic import CreateView, ListView, UpdateView
from ..check_answer import binary_class


class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


@method_decorator([login_required, ], name='dispatch')
class CompetitionView(ListView):
    model = Competition
    ordering = ('date_of_start',)
    context_object_name = 'competitions'
    template_name = './teachers/competition_list.html'

    def get_queryset(self):
        user = self.request.user
        queryset = Competition.objects.all().filter(author=user)
        return queryset



@login_required
def one_competition(request, pk):
    competition = get_object_or_404(Competition, pk=pk)
    maybeColabHref = 0
    try:
        maybeColabHref = ColabHref.objects.all().filter(competition=competition).select_related('student')
    except:
        print("maybeComp not")
    answerFiles = 0
    try:
        answerFiles = AnswerFile.objects.filter(competition=competition).select_related('student', 'student__user')
    except:
        print("answerFiles not")
    points = 0
    try:
        points = TakenCompetitionn.objects.filter(competition=competition).select_related('student',
                                                                                          'student__user').order_by(
            '-student')
    except:
        print("answerFiles not")
    competitionfile = 0
    try:
        competitionfile = CompetitionFile.objects.get(competition=competition)
    except:
        print("competitionfile not")
    subject = competition.subject.name
    author = competition.author.username

    if maybeColabHref != 0:
        if answerFiles != 0:
            return render(request, './teachers/one_comp.html', {

                'subject': subject,
                'competition': competition,
                'colabHref': maybeColabHref,
                'answerFiles': answerFiles,
                'competitionfile': competitionfile,
                'points':points,
            })
        else:
            return render(request, './teachers/one_comp.html', {

                'subject': subject,
                'competition': competition,
                'colabHref': maybeColabHref,
                'competitionfile': competitionfile,
                'points': points,
            })
    else:
        if answerFiles != 0:
            return render(request, './teachers/one_comp.html', {

                'subject': subject,
                'competition': competition,
                'answerFiles': answerFiles,
                'competitionfile': competitionfile,
                'points': points,
            })
        else:
            return render(request, './teachers/one_comp.html', {

                'subject': subject,
                'competition': competition,
                'competitionfile': competitionfile,
                'points': points,
            })


@login_required
def add_new_competition(request):
    if request.method == 'POST':
        print(request.POST)
        comp_name = request.POST['name']
        comp_desc = request.POST['desc']
        comp_subject = request.POST['subject']
        subject = get_object_or_404(Subject, name=comp_subject)
        comp_state = request.POST['state']
        comp_complexity = request.POST['complexity']
        test_file = request.POST['test_file']
        data_file = request.POST['data_file']
        true_answer_file = request.POST['true_answer_file']
        competition = Competition.objects.create(name=comp_name, desc=comp_desc, author_id=request.user.id,
                                                 subject_id=subject.id,
                                                 state=comp_state, complexity=comp_complexity)
        CompetitionFile.objects.create(competition_id=competition.id, test_file=test_file, data_file=data_file,
                                       true_answer_file=true_answer_file)
        return redirect('teachers:competition_list')
    else:
        return render(request, './teachers/ad_new_competition.html', {
            'form': AddNewCompetitionForm(),
            'form1': AddCompetitionFileForm(),
        })
