from django.urls import include, path

from .views import classroom, students, companies

urlpatterns = [
    path('', classroom.home, name='home'),

    path('students/', include(([
        # path('', students.VacancyListView.as_view(), name='quiz_list'),
        path('', students.StudentProfileView.as_view(), name='student_profile'),
        path('interests/', students.StudentInterestsView.as_view(), name='student_interests'),
        path('taken/', students.TakenQuizListView.as_view(), name='taken_quiz_list'),
        # path('quiz/<int:pk>/', students.take_quiz, name='take_quiz'),
    ], 'classroom'), namespace='students')),

    path('companies/', include(([
        path('', companies.VacancyListView.as_view(), name='quiz_change_list'),
        path('quiz/add/', companies.VacancyCreateView.as_view(), name='quiz_add'),
        path('quiz/<int:pk>/', companies.VacancyUpdateView.as_view(), name='quiz_change'),
        path('quiz/<int:pk>/delete/', companies.VacancyDeleteView.as_view(), name='quiz_delete'),
        path('quiz/<int:pk>/results/', companies.QuizResultsView.as_view(), name='quiz_results'),
        # path('quiz/<int:pk>/question/add/', companies.vacancy_add, name='vacancy_add'),
        # path('quiz/<int:quiz_pk>/question/<int:question_pk>/', companies.question_change, name='question_change'),
        # path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', companies.QuestionDeleteView.as_view(), name='question_delete'),
    ], 'classroom'), namespace='companies')),
]
