from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView

from ..decorators import student_required
from ..forms import StudentCourseForm, StudentSignUpForm
from ..models import Student, Course, Faculty, Department, Speciality, \
    User, Vacancy, StudentVacancy


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'студент'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('students:student_profile')


@method_decorator([login_required, student_required], name='dispatch')
class StudentProfileView(ListView):
    model = Student
    # ordering = ('',)
    context_object_name = 'student_profile'
    template_name = 'classroom/student.html'


@method_decorator([login_required, student_required], name='dispatch')
class StudentProfileEdit(UpdateView):
    """
    тут менять курс у студента
    TODO: добавить вещи
    """
    model = Student
    form_class = StudentCourseForm
    template_name = 'classroom/students/interests_form.html'
    success_url = reverse_lazy('students:student_profile')

    def get_object(self):
        return self.request.user.student

    def form_valid(self, form):
        messages.success(self.request, 'Interests updated with success!')
        return super().form_valid(form)


# @method_decorator([login_required, student_required], name='dispatch')
# class VacancyListView(ListView):
#     model = Vacancy
#     ordering = ('title',)
#     context_object_name = 'vacancies'
#     template_name = 'classroom/vacancy.html'

    # def get_queryset(self):
    #     student = self.request.user.student
    #     student_course = student.course
    #     student_faculty = student.faculty
    #     student_department = student.department
    #     student_speciality = student.speciality
    #     responded_vacancies = student.responded_vacancies.values_list('pk', flat=True)
    #     queryset = Vacancy.objects.filter(cource=student_course) \
    #         .exclude(pk__in=responded_vacancies)
    #         # .annotate(questions_count=Count('questions')) \
    #         # .filter(questions_count__gt=0)
    #     return queryset


@method_decorator([login_required, student_required], name='dispatch')
class TakenQuizListView(ListView):
    model = StudentVacancy
    context_object_name = 'responded_vacancies'
    template_name = 'classroom/students/taken_quiz_list.html'

    def get_queryset(self):
        queryset = self.request.user.student.responded_vacancies \
            .select_related('vacancy', 'vacancy__course') \
            .order_by('vacancy__name')
        return queryset


@login_required
@student_required
def take_vacancy(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk)
    student = request.user.student

    # if student.quizzes.filter(pk=pk).exists():
    #     return render(request, 'students/taken_quiz.html')
    #
    # total_questions = quiz.questions.count()
    # unanswered_questions = student.get_unanswered_questions(quiz)
    # total_unanswered_questions = unanswered_questions.count()
    # progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100)
    # question = unanswered_questions.first()
    #
    # if request.method == 'POST':
    #     form = TakeQuizForm(question=question, data=request.POST)
    #     if form.is_valid():
    #         with transaction.atomic():
    #             student_answer = form.save(commit=False)
    #             student_answer.student = student
    #             student_answer.save()
    #             if student.get_unanswered_questions(quiz).exists():
    #                 return redirect('students:take_quiz', pk)
    #             else:
    #                 correct_answers = student.quiz_answers.filter(answer__question__quiz=quiz, answer__is_correct=True).count()
    #                 score = round((correct_answers / total_questions) * 100.0, 2)
    #                 TakenQuiz.objects.create(student=student, quiz=quiz, score=score)
    #                 if score < 50.0:
    #                     messages.warning(request, 'Better luck next time! Your score for the quiz %s was %s.' % (quiz.name, score))
    #                 else:
    #                     messages.success(request, 'Congratulations! You completed the quiz %s with success! You scored %s points.' % (quiz.name, score))
    #                 return redirect('students:quiz_list')
    # else:
    #     form = TakeQuizForm(question=question)
    #
    # return render(request, 'classroom/students/take_quiz_form.html', {
    #     'quiz': quiz,
    #     'question': question,
    #     'form': form,
    #     'progress': progress
    # })
