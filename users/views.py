from django.shortcuts import redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from main.models import CourseEnrollment, Course


@login_required(login_url='/auth/login/')  # Aniq login URL ko'rsatish
def dashboard(request):
    enrollments = CourseEnrollment.objects.filter(user=request.user)
    courses = Course.objects.all()
    return render(request, "users/dashboard.html", {
        "user": request.user,
        "enrollments": enrollments,
        "courses": courses
    })

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})