from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.urls import reverse_lazy
from .models import Task
from .forms import CustomUserCreationForm
from django.db.models import Q

# Function-based view for user registration
def register(request):
    # Handle form submission
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)  # Authenticate the user
            login(request, user)  # Log in the user
            return redirect('task-list')  # Redirect to the task list page
    else:
        form = CustomUserCreationForm()  # Create an empty form instance for GET requests
    return render(request, 'auth/register.html', {'form': form})

# Class-based view for listing tasks, requires user to be logged in
@method_decorator(login_required, name='dispatch')
class TaskList(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'base/task_list.html'

    # Filter tasks to only show those belonging to the current user
    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        # Optional filtering by priority if specified in GET parameters
        priority = self.request.GET.get('priority', None)
        if priority:
            queryset = queryset.filter(priority=priority)
        search_query = self.request.GET.get('search', None)
        
        # Search by task title or description
        if search_query:
           queryset = queryset.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )
        return queryset

# Class-based view for showing task details, requires user to be logged in
@method_decorator(login_required, name='dispatch')
class TaskDetail(DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'

    def get_object(self, queryset=None):
        task = super().get_object(queryset)
        if task.user != self.request.user:
            raise PermissionDenied("You do not have permission to view this task.")
        return task

# Class-based view for creating a new task, requires user to be logged in
@method_decorator(login_required, name='dispatch')
class TaskCreate(CreateView):
    model = Task
    fields = ['title', 'description', 'due_date', 'priority']
    success_url = reverse_lazy('task-list')
    template_name = 'base/task_form.html'

    # # Automatically assign the current user to the new task
    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     return super().form_valid(form)

# Class-based view for updating an existing task, requires user to be logged in
@method_decorator(login_required, name='dispatch')
class TaskUpdate(UpdateView):
    model = Task
    fields = ['title', 'description', 'due_date', 'priority', 'complete']
    success_url = reverse_lazy('task-list')
    template_name = 'base/task_form.html'

    # Ensure the task belongs to the current user
    def get_object(self, queryset=None):
        task = super().get_object(queryset)
        if task.user != self.request.user:
            raise PermissionDenied
        return task

# Class-based view for deleting a task, requires user to be logged in
@method_decorator(login_required, name='dispatch')
class TaskDelete(DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('task-list')
    template_name = 'base/task_confirm_delete.html'

    # Ensure the task belongs to the current user
    def get_object(self, queryset=None):
        task = super().get_object(queryset)
        if task.user != self.request.user:
            raise PermissionDenied
        return task
    