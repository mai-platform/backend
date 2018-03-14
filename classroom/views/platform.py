from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_company:
            return redirect('companies:quiz_change_list')
        else:
            return redirect('students:student_profile')
    return render(request, 'classroom/index.html')
