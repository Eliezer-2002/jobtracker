from django.shortcuts import render, redirect
from .models import Job
from .forms import JobForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from datetime import datetime, timedelta


@login_required
def job_list(request):
    jobs = Job.objects.filter(user=request.user)

    for job in jobs:
        if datetime.now().date() - job.last_updated.date() > timedelta(days=1):
            job.follow_up = True
        else:
            job.follow_up = False

    return render(request, "jobs/job_list.html", {"jobs": jobs})


@login_required
def add_job(request):
    form = JobForm(request.POST or None)
    if form.is_valid():
        job = form.save(commit=False)
        job.user = request.user
        job.save()
        return redirect("job_list")
    return render(request, "jobs/add_job.html", {"form": form})


@login_required
def update_job(request, id):
    job = Job.objects.get(id=id)
    form = JobForm(request.POST or None, instance=job)
    if form.is_valid():
        form.save()
        return redirect("job_list")
    return render(request, "jobs/add_job.html", {"form": form})


@login_required
def delete_job(request, id):
    job = Job.objects.get(id=id)
    job.delete()
    return redirect("job_list")


# AUTH


def register(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("job_list")
    return render(request, "jobs/register.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("login")

@login_required
def generate_cover_letter(request, id):
    job = Job.objects.get(id=id)

    # Simple AI (mock for now)
    cover_letter = f"""
    Dear Hiring Manager,

    I am excited to apply for the {job.title} position at {job.company}.
    My skills and experience make me a strong fit for this role.

    I look forward to contributing to your team.

    Sincerely,
    {request.user.username}
    """

    return render(
        request, "jobs/cover_letter.html", {"cover_letter": cover_letter, "job": job}
    )
