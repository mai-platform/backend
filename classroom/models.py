from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)


#######################################
########### General models ############
#######################################

class Course(models.Model):
    """
    Минимальный курс, с которого студента возьмут на практику.
    В шаблоне обрабатывать в виде 'course.min и выше'.
    """
    min = models.IntegerField(default=2)

    def __str__(self):
        return self.min


class Faculty(models.Model):
    # TODO: сделать модели зависимыми: факультет -> кафедра -> специальность
    """
    Факультет студента. Значения по умолчанию задать через миграции.
    """
    number = models.IntegerField()
    title = models.CharField(max_length=40)

    def __str__(self):
        return self.title


class Department(models.Model):
    """
    Кафедра студента. Значения по умолчанию задать через миграции.
    """
    number = models.IntegerField()
    title = models.CharField(max_length=40)

    def __str__(self):
        return self.title


class Speciality(models.Model):
    """
    Специальность студента. Значения по умолчанию задать через миграции.
    """
    title = models.CharField(max_length=40)

    def __str__(self):
        return self.title


#######################################
####### Vacancy related models ########
#######################################

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


class Quiz(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    name = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='quizzes')

    def __str__(self):
        return self.name


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField('Question', max_length=255)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField('Answer', max_length=255)
    is_correct = models.BooleanField('Correct answer', default=False)

    def __str__(self):
        return self.text


class Vacancy(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vacancies')
    title = models.CharField('Title', max_length=40)
    course = models.ForeignKey(Course, related_name='vacancy_course', on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, related_name='vacancy_faculty', on_delete=models.CASCADE)
    department = models.ForeignKey(Department, related_name='vacancy_department', on_delete=models.CASCADE)
    speciality = models.ForeignKey(Speciality, related_name='vacancy_speciality', on_delete=models.CASCADE)
    descriprion = models.TextField(max_length=300, blank=False)


#######################################
####### Student related models ########
#######################################

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    course = models.ForeignKey(Course, related_name='student_course', on_delete=models.CASCADE, null=True)
    faculty = models.ForeignKey(Faculty, related_name='student_faculty', on_delete=models.CASCADE, null=True)
    department = models.ForeignKey(Department, related_name='student_department', on_delete=models.CASCADE, null=True)
    speciality = models.ForeignKey(Speciality, related_name='student_speciality', on_delete=models.CASCADE, null=True)

    # def get_unanswered_questions(self, quiz):
    #     answered_questions = self.quiz_answers \
    #         .filter(answer__question__quiz=quiz) \
    #         .values_list('answer__question__pk', flat=True)
    #     questions = quiz.questions.exclude(pk__in=answered_questions).order_by('text')
    #     return questions

    def get_responded_vacancy(self, vacancy):
        responded_vacancy = self.responded_vacancies \
            .filter()
        return responded_vacancy

    def __str__(self):
        return self.user.username


class StudentVacancy(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='responded_vacancies')
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='+')
    date = models.DateTimeField(auto_now_add=True)


# class TakenVacancy(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='taken_vacancies')
#     vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='taken_vacancies')
#     date = models.DateTimeField()

# class TakenQuiz(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='taken_quizzes')
#     quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken_quizzes')
#     score = models.FloatField()
#     date = models.DateTimeField(auto_now_add=True)
#
#
# class StudentAnswer(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quiz_answers')
#     answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+')
