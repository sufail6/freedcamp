import pdb

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Count, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import UpdateView

from app.forms import Add_List_Form, TaskForm, Project_form, CreateForm, ProfileUpdateForm, TaskUpdateForm, StatusForm, \
    AssignForm, PriorityForm
from app.models import Add_Lists, Tasks, Projects, Create


def home(request):
    return render(request, 'home.html')


@method_decorator(login_required(login_url='login'), name='dispatch')
class ProjectView(View):
    def get(self, request):
        form = Project_form()
        data = Projects.objects.all()
        return render(request, 'project.html', {'form': form, 'data': data})

    def post(self, request):
        form = Project_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('project')
        else:
            data = Projects.objects.all()
            return render(request, 'project.html', {'form': form, 'data': data})


def user_register(request):
    if request.method == 'GET':
        form = CreateForm()
        context = {'form': form}
        return render(request, 'user_register.html', context)

    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('project')
            else:
                messages.error(request, 'Authentication Failed')
        else:
            messages.error(request, 'Error Processing Your Request')
        context = {'form': form}
        return render(request, 'user_register.html', context)

    return render(request, 'user_register.html', {})


@login_required(login_url='login')
def profile(request):
    return render(request, 'copy.html')


def log_out(request):
    logout(request)
    return redirect('login')


def copy(request):
    return render(request, 'copy.html')


@login_required(login_url='login')
def profile_view(request):
    user_profile = Create.objects.get(email=request.user.email)
    return render(request, 'project.html', {'user_profile': user_profile})


#
# def profile_update(request, id):
#     data = Create.objects.get(id=id)
#     if request.method == 'POST':
#         form = ProfileUpdateForm(request.POST or None, request.FILES, instance=data)
#         if form.is_valid():
#             form.save()
#             return redirect('project')
#     else:
#         form = ProfileUpdateForm(instance=data)
#     return render(request, 'profile_update.html', {'form': form})

@login_required(login_url='login')
def profile_update(request, pk=None):
    user = get_object_or_404(Create, id=request.user.id)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('project')
    else:
        form = ProfileUpdateForm(instance=user)
    return render(request, 'profile_update.html', {'form': form})


def test(request):
    return render(request, 'test/main.html')


# def index(request, *args, **kwargs):
#     # handle POST request to add a new list
#     id = kwargs['id']
#     print(id)
#     if request.method == 'POST':
#         form = Add_List_Form(request.POST, request.FILES)
#         project_data = Projects.objects.get(id=id)
#         Add_Lists.objects.create(name=request.POST['name'], description=request.POST['description'],
#                                  project=project_data)
#         if form.is_valid():
#             print('valid')
#             pass
#         #     print('valid')
#         #     # formsave = form.save()
#         #     pdb.set_trace()
#         #     # formsave = Add_Lists.objects.create(name=)
#         #     print('valid')
#         #     formsave.project = id
#         #     formsave.save()
#         #     print('save')
#         #     return redirect('/index/' + str(id) + '/')
#         #
#         else:
#             print('else1')
#             task = TaskForm(request.POST, request.FILES)
#             if task.is_valid():
#                 task.save()
#                 # return redirect('index/<int:id>/')
#     # handle GET request to display existing lists
#     else:
#         print('else')
#         form = Add_List_Form()
#         data = Add_Lists.objects.filter(project_id=id)
#         tasks = TaskForm()
#         # modify the add variable to retrieve only the tasks related to the current Add_Lists instance
#         add = data.first().tasks.all() if data else None
#         return render(request, 'project_details.html', {'form': form, 'data': data, 'tasks': tasks, 'add': add,
#                                                         'project_id': id})
#
#     return HttpResponse("Something went wrong")


def index(request, *args, **kwargs):
    # handle POST request to add a new list
    id = kwargs['id']
    if request.method == 'POST':
        action = request.GET.get('action')
        if action == 'add_list':
            form = Add_List_Form(request.POST, request.FILES)
            project_data = Projects.objects.get(id=id)
            Add_Lists.objects.create(name=request.POST['name'], description=request.POST.get('description', ''),
                                     project=project_data)
            if form.is_valid():
                pass
        elif action == 'task':
            # pdb.set_trace()
            Tasks.objects.create(name_id=request.POST['add_list'], title=request.POST['title'],
                                 description=request.POST['description'],
                                 assigned_to_id=request.POST['assigned_to'], status=request.POST['status'],
                                 priority=request.POST['priority'],
                                 attachment=request.FILES.get('attachment'))

            task = TaskForm(request.POST, request.FILES)
            if task.is_valid():
                task.save()
        return redirect('/index/' + str(id) + '/')
    # handle GET request to display existing lists
    else:
        form = Add_List_Form()
        project_data = Projects.objects.get(id=id)
        task_list = Tasks.objects.all().order_by('-id')
        project = Projects.objects.all()

        # get search query from request GET parameter
        search_query = request.GET.get('q', '')

        # filter Add_Lists instances by project id and search query
        data = Add_Lists.objects.prefetch_related('tasks').filter(
            Q(project_id=id) & Q(name__icontains=search_query)
        ).order_by('-id')

        tasks = TaskForm()
        status = StatusForm()
        assign = AssignForm
        priority = PriorityForm()
        add = data.first().tasks.all() if data else None

        return render(request, 'project_details.html', {
            'form': form,
            'data': data,
            'tasks': tasks,
            'add': add,
            'project_id': id,
            'project_data': project_data,
            'task_list': task_list,
            'search_query': search_query,
            'project': project,
            'status': status,
            'assign': assign,
            'priority': priority,

        })


def index_test(request):
    return render(request, 'test/indextest.html')


# def delete_list(request, pk=None):
#     data = Add_Lists.objects.get(pk=pk)
#     project_id = data.project.id  # get the project id before deleting the data
#     if request.method == 'POST':
#         data.delete()
#         return redirect('index', id=project_id)
#     else:
#         return redirect('index', id=project_id)
from django.http import JsonResponse


def delete_list(request, pk=None):
    data = Add_Lists.objects.get(pk=pk)
    project_id = data.project.id  # get the project id before deleting the data
    if request.method == 'POST':
        data.delete()
        return JsonResponse({'success': True})
    else:
        return redirect('index', id=project_id)


# def task_update(request, id):
#     data = Tasks.objects.get(id=id)
#     if request.method == 'POST':
#         form = TaskForm(request.POST or None, request.FILES, instance=data)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#     else:
#         form = TaskForm(instance=data)
#     return render(request, 'task_update.html', {'form': form})

@login_required(login_url='login')
def task_update(request, id):
    data = Tasks.objects.get(id=id)
    if request.method == 'POST':
        form = TaskUpdateForm(request.POST or None, request.FILES, instance=data)
        if form.is_valid():
            form.save()
            return redirect('/index/{}/'.format(data.name.project.id))
    else:
        form = TaskForm(instance=data)
    return render(request, 'task_update.html', {'form': form})


# def add_attachment(request, id):
#     data = Tasks.objects.get(id=id)
#     if request.method == 'POST':
#         form = AddAttachmentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/index/{}/'.format(data.name.project.id))
#         else:
#             messages.info(request, '')
#     else:
#         form = AddAttachmentForm()
#     return render(request, 'add_attachment.html',{'form':form})


def delete_project_ajax(request, id):
    try:
        data = Projects.objects.get(id=id)
        data.delete()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error'})


def status_update(request, id):
    data = get_object_or_404(Tasks, id=id)
    project_id = data.name.project.id  # Get the project ID from the data object
    task_id = data.id
    print(task_id)
    if request.method == 'POST':
        form = StatusForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form.save()
            return redirect('/index/{}/'.format(project_id))  # Use the project_id variable in the redirect URL
    else:
        print('else')
        form = StatusForm(instance=data)

    return render(request, 'index.html', {'form': form, 'project_id': project_id, 'task_id': task_id})


def priority_update(request, id):
    data = get_object_or_404(Tasks, id=id)
    project_id = data.name.project.id
    task_id = data.id
    if request.method == 'POST':
        form = PriorityForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form.save()
            return redirect('/index/{}/'.format(project_id))  # Use the project_id variable in the redirect URL
    else:
        form = PriorityForm(instance=data)
    return render(request, 'index.html', {'form': form, 'project_id': project_id, 'task_id': task_id})


def assign_update(request, id):
    data = get_object_or_404(Tasks, id=id)
    project_id = data.name.project.id
    task_id = data.id
    if request.method == 'POST':
        form = AssignForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form.save()
            return redirect('/index/{}/'.format(project_id))  # Use the project_id variable in the redirect URL
    else:
        form = AssignForm(instance=data)
    return render(request, 'index.html', {'form': form, 'project_id': project_id, 'task_id': task_id})