from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.views.generic import RedirectView
from django.contrib.auth.models import User

from .models import Question, Answer, Category
from .forms import AskForm, AnswerForm, CategoryForm


def home(request, a_id=None):
    new_questions = Question.objects.new()
    top = Question.objects.popular(5)
    pref = ''
    title = 'Main Page: Most Recent'

    if 'popular' in request.path:
        new_questions = Question.objects.popular()
        pref = '/popular/'
        title = 'Most Popular'

    if 'author' in request.path and a_id:
        auth = get_object_or_404(User, id=a_id)
        new_questions = auth.question_set.new()
        title = f'Questions by {auth.username}'

    if 'category' in request.path and a_id:
        cat = get_object_or_404(Category, id=a_id)
        new_questions = cat.question_set.new()
        title = f'Category: {cat.name}'

    if 'search' in request.GET:
        search_term = request.GET['search']
        new_questions = new_questions.filter(title__icontains=search_term) | \
                        new_questions.filter(text__icontains=search_term)
        title = f'Search results for {search_term}'

    limit = request.GET.get('limit', 10)
    page = int(request.GET.get('page', 1))
    paginator = Paginator(new_questions, limit)
    paginator.baseurl = pref + '?page='

    try:
        questions = paginator.page(page)

    except EmptyPage:

        questions = paginator.page(paginator.num_pages)

    return render(request, 'questions.html', {
        'questions': questions,
        'paginator': paginator,
        'title': title,
        'top': top,
        'top_categories': Category.objects.popular_categories(),
    })


def question (request, qn_id):
    qn = get_object_or_404(Question, id=qn_id)
    top = Question.objects.popular(5)
    answers = qn.answer_set.filter(active=True, parent__isnull=True)
    ans_form = AnswerForm()

    if request.method == 'POST':
        if request.user.is_authenticated:
            ans_form = AnswerForm(request.POST)

            if ans_form.is_valid():

                try:
                    parent_id = request.POST.get('parent_id')
                except (KeyError,):
                    parent_id = None

                if parent_id:
                    parent_obj = Answer.objects.get(id=parent_id)
                    if parent_obj:
                        reply_answer = ans_form.save(commit=False)
                        reply_answer.parent = parent_obj  # assign parent_obj to reply

                ans_form = ans_form.save(commit=False)
                ans_form.author = request.user
                ans_form.question = qn
                ans_form.save()

            return redirect('qa:question')

        else:
            m = messages.warning(request, 'Sorry! You have to login first!')
            return redirect(f'/users/login?next={qn.get_url()}', m)

    return render(request, 'question.html', {'qn': qn, 'answers': answers,
                                             'ans_form': ans_form, 'top': top,
                                             'top_categories': Category.objects.popular_categories(), })


class QuestionLikeRedirect(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        qn_id = self.kwargs.get('qn_id')
        qn = get_object_or_404(Question, id=qn_id)
        url_ = qn.get_url()
        user = self.request.user

        if user.is_authenticated:

            if user in qn.likes.all():
                qn.likes.remove(user)
                qn.rating -= 1
            else:
                qn.likes.add(user)
                qn.rating += 1

            qn.save()

        return url_


class QAnsweredRedirect(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        a_id = self.kwargs.get('a_id')
        ans = get_object_or_404(Answer, id=a_id)
        url_ = ans.question.get_url()
        user = self.request.user
        if user.is_authenticated and user == ans.question.author:
            if ans.best_answer:
                ans.best_answer = False
            else:
                ans.best_answer = True
            ans.save()
        return url_


@login_required
def ask(request):
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.author = request.user
            f.save()

            form.save_m2m()
            m = messages.success(request, 'OK! The question was created')
            return redirect(f.get_url(), m)
    else:
        form = AskForm()

    return render(request, 'askform.html', {'form': form})


@login_required
def delete(request, obj_type, o_id):
    choose = {'q': [Question, 'question', '/'],
              'a': [Answer, 'answer', ''],
              'c': [Category, 'category', '/categories'], }
    try:
        obj = get_object_or_404(choose[obj_type][0], id=o_id)
        permission = True if obj_type == 'c' else obj.author == request.user
        if request.method == "POST" and permission:
            obj.delete()
            m = messages.success(request, f'OK! The {choose[obj_type][1]} was deleted')
            return HttpResponseRedirect(choose[obj_type][2], m) if obj_type in ['q', 'c'] \
                else redirect(obj.question.get_url(), m)
    except (KeyError,):
        return redirect('/')


@login_required
def edit(request, obj_type, o_id):
    choose = {'q': [Question, AskForm, 'qa/askform.html', 'question'],
              'a': [Answer, AnswerForm, 'qa/edit.html', 'answer'],
              'c': [Category, CategoryForm, 'qa/askform.html', 'category']}

    try:
        obj = get_object_or_404(choose[obj_type][0], id=o_id)
        permission = True if obj_type == 'c' else obj.author == request.user
        red = '/categories'

        if request.method == "POST" and permission:
            form = choose[obj_type][1](request.POST, instance=obj)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.added_at = timezone.now()
                m = messages.success(request, f"The {choose[obj_type][3]} was successfully edited")
                obj.save()
                form.save_m2m()

                if obj_type != 'c':
                    red = obj.get_url() if obj_type == 'q' else obj.question.get_url()

                return HttpResponseRedirect(red, m)
        else:
            form = choose[obj_type][1](instance=obj)

        return render(request, choose[obj_type][2], {'form': form})

    except (KeyError,):
        raise Http404


@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            m = messages.success(request, f'Success! You\'ve just created a new category!')
            return HttpResponseRedirect('/categories', m)
    else:
        form = CategoryForm()

    return render(request, 'askform.html', {'form': form})


def serve_categories(request):
    cat = Category.objects.all().order_by('id')
    top = Question.objects.popular(5)

    title = 'Categories'
    limit = request.GET.get('limit', 10)
    page = int(request.GET.get('page', 1))
    paginator = Paginator(cat, limit)
    paginator.baseurl = '?page='
    categories = paginator.page(page)

    return render(request, 'categories.html', {'categories': categories,
                                               'paginator': paginator,
                                               'title': title,
                                               'top': top,
                                               'top_categories': Category.objects.popular_categories(), })


@login_required
def activity(request, auth_id):
    auth = get_object_or_404(User, id=auth_id)

    if request.user.id == auth.id:

        my_questions = Question.objects.filter(author=auth)
        my_answers = Answer.objects.filter(author=auth)

        my_starred = Question.objects.get_starred(auth)

        return render(request, 'activity.html', {'title': f'{auth.username}\'s personal page',
                                                 'my_questions': my_questions,
                                                 'my_answers': my_answers,
                                                 'my_starred': my_starred})
    else:
        return HttpResponseRedirect('/', messages.warning(request, 'Oooups! The Wrong Way!'))
