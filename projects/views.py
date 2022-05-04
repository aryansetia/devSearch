from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project, Tag
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .utils import searchProject
from django.core.paginator import Paginator
# Create your views here.


def projects(request):
    projects, text = searchProject(request)

    page = request.GET.get('page')
    results = 3
    paginator = Paginator(projects, results)

    projects = paginator.page(page)

    context = {'projects': projects, 'text':text}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    print('projectObj:', projectObj)
    return render(request, 'projects/single-project.html', {'project': projectObj})

@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')

    context = {'form':form}
    return render(request, 'projects/project_forms.html', context)

@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form':form}
    return render(request, 'projects/project_forms.html', context)

@login_required(login_url='login')
def deleteProject(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {'object':project}
    return render(request, 'delete_template.html',context)