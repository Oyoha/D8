from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import *
from .filters import PostSearch
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-public_time')
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/news/')


class NewDetailView(DetailView):
    template_name = 'new.html'
    queryset = Post.objects.all()


class NewsFilter(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostSearch(self.request.GET, queryset=self.get_queryset())
        return context


class NewsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'new_create.html'
    form_class = PostForm
    permission_required = ('News.add_post')


class NewUpgradeView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'new_create.html'
    form_class = PostForm
    permission_required = ('News.change_product')

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'new_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
