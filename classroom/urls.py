from django.urls import include, path

from .views import platform, students, companies, vacancies

urlpatterns = [
    path('', platform.home, name='home'),

    path('vacancy/', include(([
path('', vacancies.VacanciesListView.as_view(), name='vacancies_list'),
    ], 'classroom'), namespace='vacancy')),

    path('students/', include(([

        path('me', students.StudentProfileView.as_view(), name='student_profile'),
        path('edit/', students.StudentProfileEdit.as_view(), name='student_interests'),
    ], 'classroom'), namespace='students')),

    path('companies/', include(([
        path('', companies.VacancyListView.as_view(), name='quiz_change_list'),
        path('quiz/add/', companies.VacancyCreateView.as_view(), name='quiz_add'),
        path('quiz/<int:pk>/', companies.VacancyUpdateView.as_view(), name='quiz_change'),
        path('quiz/<int:pk>/delete/', companies.VacancyDeleteView.as_view(), name='quiz_delete'),
        path('quiz/<int:pk>/results/', companies.QuizResultsView.as_view(), name='quiz_results'),
    ], 'classroom'), namespace='companies')),
]
