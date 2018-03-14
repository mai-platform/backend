from django.urls import include, path

from classroom.views import platform, students, companies

urlpatterns = [
    path('', include('classroom.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', platform.SignUpView.as_view(), name='signup'),
    path('accounts/signup/student/', students.StudentSignUpView.as_view(), name='student_signup'),
    path('accounts/signup/company/', companies.CompanySignUpView.as_view(), name='company_signup'),
]
