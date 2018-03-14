from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

# from classroom.models import (Answer, Question, Student, StudentAnswer,
#                               Subject, User)

from classroom.models import (Course, Faculty, Department, Speciality,
                              Vacancy, Student, User)


class CompanySignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_company = True
        if commit:
            user.save()
        return user


class StudentSignUpForm(UserCreationForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), required=True)
    faculty = forms.ModelChoiceField(queryset=Faculty.objects.all(), required=True)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=True)
    speciality = forms.ModelChoiceField(queryset=Speciality.objects.all(), required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2", "course", "faculty", "department", "speciality")

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        student.course.add(*self.cleaned_data.get('course'))
        student.faculty.add(*self.cleaned_data.get('faculty'))
        student.department.add(*self.cleaned_data.get('department'))
        student.speciality.add(*self.cleaned_data.get('speciality'))
        return user


class StudentCourseForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('course', )
        widgets = {
            'course': forms.CheckboxSelectMultiple
        }


class VacancyForm(forms.ModelForm):
    # course = forms.ModelChoiceField(queryset=Course.objects.all(), required=True)
    # faculty = forms.ModelChoiceField(queryset=Faculty.objects.all(), required=True)
    # department = forms.ModelChoiceField(queryset=Department.objects.all(), required=True)
    # speciality = forms.ModelChoiceField(queryset=Speciality.objects.all(), required=True)
    # class Meta:
    #     model = Vacancy
    #     fields = ('title', 'descriprion', 'course', 'faculty', 'department')
    #     widgets = {
    #         'descriprion': forms.TextInput,
    #         'course': forms.ChoiceField,
    #         'faculty': forms.ChoiceField,
    #         'department': forms.ChoiceField,
    #     }
    pass


# class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
#     def clean(self):
#         super().clean()
#
#         has_one_correct_answer = False
#         for form in self.forms:
#             if not form.cleaned_data.get('DELETE', False):
#                 if form.cleaned_data.get('is_correct', False):
#                     has_one_correct_answer = True
#                     break
#         if not has_one_correct_answer:
#             raise ValidationError('Mark at least one answer as correct.', code='no_correct_answer')


# class TakeQuizForm(forms.ModelForm):
#     answer = forms.ModelChoiceField(
#         queryset=Answer.objects.none(),
#         widget=forms.RadioSelect(),
#         required=True,
#         empty_label=None)
#
#     class Meta:
#         model = StudentAnswer
#         fields = ('answer', )
#
#     def __init__(self, *args, **kwargs):
#         question = kwargs.pop('question')
#         super().__init__(*args, **kwargs)
#         self.fields['answer'].queryset = question.answers.order_by('text')
