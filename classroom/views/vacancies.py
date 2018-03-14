from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DetailView

from ..decorators import student_required
from ..forms import StudentCourseForm, StudentSignUpForm
from ..models import Student, Course, Faculty, Department, Speciality, \
    User, Vacancy, StudentVacancy

# @method_decorator([login_required, student_required], name='dispatch')
# class StudentProfileView(ListView):
#     model = Student
#     # ordering = ('',)
#     context_object_name = 'student_profile'
#     template_name = 'classroom/student.html'


@method_decorator([login_required], name='dispatch')
class VacanciesListView(ListView):
    model = Vacancy
    ordering = ('title',)
    context_object_name = 'vacancies_list'
    template_name = 'classroom/vacancy.html'


# @method_decorator([login_required], name='dispatch')
# class VacancyView(DetailView):
#     model = Vacancy
#     context_object_name = 'vacancy'
#     template_name = 'classroom/vacancy.html'