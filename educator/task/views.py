import random

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.utils.text import slugify
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from task.models import *
from task.forms import *

MENU = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        {'title': 'Войти', 'url_name': 'login'},
        ]
NUMBER_OF_CARDS = 9


def index(request):
    random_number = random.randint(1, 100000)
    tasks = Task.objects.all()
    categories = Category.objects.all()
    subjects = Subject.objects.all()
    paginator = Paginator(tasks, NUMBER_OF_CARDS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'title': 'Главная страница',
        'menu': MENU,
        'categories': categories,
        'subjects': subjects,
        'category_selected': 0,
        'random_number': random_number,
    }
    return render(request, 'task/index.html', context=context)


def category(request):
    task = Task.objects.all()
    categories = Category.objects.all()
    subjects = Subject.objects.all()
    paginator = Paginator(categories, NUMBER_OF_CARDS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Главная страница',
        'menu': MENU,
        'task': task,
        'page_obj': page_obj,
        'subjects': subjects,
        'category_selected': 0,
    }
    return render(request, 'task/category.html', context)


def category_detail(request, category_id):
    categories = Category.objects.all()
    category = get_object_or_404(Category, id=category_id)
    category_subject = Subject.objects.filter(category=category)
    subjects = Subject.objects.all()
    paginator = Paginator(category_subject, NUMBER_OF_CARDS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Детали категории',
        'categories': categories,
        'menu': MENU,
        'category': category,
        'page_obj': page_obj,
        'subjects': subjects,
    }
    return render(request, 'task/category_detail.html', context=context)


def subject(request):
    task = Task.objects.all()
    categories = Category.objects.all()
    subjects = Subject.objects.all()
    paginator = Paginator(subjects, NUMBER_OF_CARDS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Главная страница',
        'menu': MENU,
        'task': task,
        'categories': categories,
        'page_obj': page_obj,
        'category_selected': 0,
    }
    return render(request, 'task/subject.html', context=context)


def subject_detail(request, subject_id):
    categories = Category.objects.all()
    subjects = Subject.objects.all()
    subject = get_object_or_404(Subject, pk=subject_id)
    tasks = Task.objects.filter(subject=subject_id)
    paginator = Paginator(tasks, NUMBER_OF_CARDS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': subject.title,
        'menu': MENU,
        'subject': subject,
        'page_obj': page_obj,
        'categories': categories,
        'subjects': subjects,
    }
    return render(request, 'task/subject_detail.html', context)


def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    categories = Category.objects.all()
    subjects = Subject.objects.all()
    images = TaskImage.objects.filter(task=task_id)
    comments = Comment.objects.filter(task=task_id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.task = task
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    context = {
        'title': 'Главная страница',
        'menu': MENU,
        'task': task,
        'categories': categories,
        'subjects': subjects,
        'category_selected': 0,
        'images': images,
        'comments': comments,
        'comment_form': comment_form
    }
    return render(request, 'task/task_detail.html', context=context)


def search_results(request):
    query = request.GET.get('q')
    if query:
        tasks = Task.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        categories = Category.objects.filter(title__icontains=query)
        subjects = Subject.objects.filter(title__icontains=query)

        # Create separate lists for each model
        task_results = [{'model_name': 'task', 'object': task} for task in tasks]
        category_results = [{'model_name': 'category', 'object': category} for category in categories]
        subject_results = [{'model_name': 'subject', 'object': subject} for subject in subjects]

        # Combine the lists and sort by model name
        results = task_results + category_results + subject_results
        results.sort(key=lambda x: x['model_name'])

        # Преобразуем запрос в URL-совместимый формат
        slugified_query = slugify(query)
    else:
        results = []
        slugified_query = None
    context = {
        'results': results,
        'slugified_query': slugified_query
    }
    return render(request, 'task/search_results.html', context)


# def toggle_like(request, task_id):
#     task = get_object_or_404(Task, pk=task_id)
#     user = request.user
#
#     if user.is_authenticated:
#         if task.likes.filter(id=user.id).exists():
#             task.likes.remove(user)
#         else:
#             task.likes.add(user)
#
#     return JsonResponse({'likes_count': task.likes.count()})


def load_more_comments(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    comments = Comment.objects.filter(task=task).order_by('-pub_date')[10:]

    data = []
    for comment in comments:
        data.append({
            'author': comment.author.username,
            'text': comment.text,
            'pub_date': comment.pub_date.strftime("%d %B %Y, %H:%M")
        })

    return JsonResponse(data, safe=False)


@login_required
@require_POST
def like_toggle(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    user = request.user
    try:
        like = Like.objects.get(user=user, task=task)
        like.delete()
        liked = False
    except Like.DoesNotExist:
        Like.objects.create(user=user, task=task)
        liked = True
    like_count = task.likes.count()
    return JsonResponse({'liked': liked, 'like_count': like_count})


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    tasks = Task.objects.filter(author=user)
    # Проверяем, существует ли чат между текущим пользователем и пользователем профиля
    chat = Chat.objects.filter(participants=request.user).filter(participants=user).first()
    if not chat:
        chat = Chat.objects.create()
        chat.participants.add(request.user, user)
    paginator = Paginator(tasks, NUMBER_OF_CARDS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'user': user,
        'page_obj': page_obj,
        'chat': chat,
    }
    return render(request, 'task/profile.html', context)


@login_required
def create_task(request, task_id=None):
    if task_id is not None:
        task = get_object_or_404(Task, pk=task_id)
        if task.author != request.user:
            return HttpResponseForbidden("You don't have permission to edit this task.")
    else:
        task = None

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            return redirect('task:task_detail', task_id=task.pk)
    else:
        form = TaskForm(instance=task)

    context = {
        'form': form,
        'task': task,
    }
    return render(request, 'task/create_task.html', context)


def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task:task_detail', task_id=task_id)
    else:
        form = TaskForm(instance=task)

    return render(request, 'task/edit_task.html', {'form': form, 'task': task})


def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('task:home')

    return render(request, 'task/delete_task.html', {'task': task})


@login_required
def chat_list(request):
    chats = Chat.objects.filter(participants=request.user)
    context = {
        'chats': chats
    }
    return render(request, 'task/chat_list.html', context)


@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    messages = Message.objects.filter(chat=chat)
    form = MessageForm()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            sender = request.user
            message = Message.objects.create(chat=chat, sender=sender, content=content)

    context = {
        'chat': chat,
        'messages': messages,
        'form': form,
    }
    return render(request, 'task/chat_detail.html', context)
