from django.urls import include, path
from .views import home, students, main, teachers, to_competition

# urlpatterns = [
#     path('', index, name='home'),
#     path('students/', include((
#         [path('', students.CompetitionView.as_view(), name='competition_list'),
#          ]
#         , 'catalog'), namespace='student'))
#
# ]
urlpatterns = [
    path('', home, name='home'),
    path('competitions/', to_competition, name='to_competition'),

    path('students/', include(([
                                   path('main/', students.CompetitionView.as_view(), name='competition_list'),
                                   path('room/', students.PersonalAccountView.as_view(), name='my_account'),
                                   path('add_competition/<int:pk>/', students.add_new_comp, name='add_new_competition'),
                                   path('taken/', students.TakenCompetitionListView.as_view(), name='take_competition'),
                                   # path('quiz/<int:pk>/', students.take_quiz, name='take_quiz'),
                                   path('add_decision/<int:pk>/', students.model_form_upload,
                                        name='download_answer_file'),
                                   path('down_test_data/<int:pk>', students.download_competition_test_data,
                                        name='download_test_data'),
                                   path('down_study_data/<int:pk>', students.download_competition_study_data,
                                        name='download_study_data'),
                                   path('down_model_data/<int:pk>', students.download_answer_model,
                                        name='download_model_data'),
                                   path('down_answer_data/<int:pk>', students.download_answer_data,
                                        name='download_answer_data'),
                                   path('competition/<int:pk>', students.one_competition, name='one_competition')
                               ], 'catalog'), namespace='students')),

    path('teachers/', include(([
                                   path('', teachers.CompetitionView.as_view(), name='competition_list'),
                                   path('competition/add/', teachers.add_new_competition,
                                        name='add_new_competition'),
                                   path('competition/<int:pk>', teachers.one_competition, name='one_competition')
                                   # path('quiz/<int:pk>/', teachers.QuizUpdateView.as_view(), name='quiz_change'),
                                   # path('quiz/<int:pk>/delete/', teachers.QuizDeleteView.as_view(), name='quiz_delete'),
                                   # path('quiz/<int:pk>/results/', teachers.QuizResultsView.as_view(), name='quiz_results'),
                                   # path('quiz/<int:pk>/question/add/', teachers.question_add, name='question_add'),
                                   # path('quiz/<int:quiz_pk>/question/<int:question_pk>/', teachers.question_change, name='question_change'),
                                   # path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', teachers.QuestionDeleteView.as_view(), name='question_delete'),
                               ], 'catalog'), namespace='teachers')),
    # path('down/', main.CreatePostView.as_view(), name='download'),
]
