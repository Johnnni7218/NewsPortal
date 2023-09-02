from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import PostForm
from .models import Author
from .models import Post
from .models import Category
from .models import Comment
from .filters import PostFilter
from .models import Entrance

class AuthorList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Author
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'user_rating'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'author.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'author'

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

class PostsList(ListView):
    model = Post
    ordering = 'time_post'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class CategoryList(ListView):
    model = Category
    ordering = 'name'
    template_name = 'category.html'
    context_object_name = 'category'

class CommentList(ListView):
    model = Comment
    ordering = 'com_rating'
    template_name = 'comment.html'
    context_object_name = 'comment'

class NewsCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        vibor = form.save(commit=False)
        vibor.vibor = 2
        return super().form_valid(form)

class PostCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        vibor = form.save(commit=False)
        vibor.vibor = 1
        return super().form_valid(form)

class NewsUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        vibor = form.save(commit=False)
        vibor.vibor = 2
        return super().form_valid(form)

class PostUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        vibor = form.save(commit=False)
        vibor.vibor = 1
        return super().form_valid(form)

class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')


# def entrance(request):
#     return render(request, 'entrance.html')

class EntranceList(ListView):
    model = Entrance
    template_name = 'entrance.html'
    context_object_name = 'entrance'

    def entrance(request):
        return render(request, 'entrance.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context

@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')

class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    massage = 'Вы подписаны на рассылку новостей категории'
    return render(request, 'subscribe.html', {'category': category, 'massage': massage})