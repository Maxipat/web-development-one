from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from blog.models import Post,Comment
from django.utils import timezone
from blog.forms import PostForm, CommentForm
from django.views.generic import(TemplateView, ListView,
                                DetailView, CreateView,
                                UpdateView, DeleteView)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class AboutView(TemplateView):
    template_name ='about.html'

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    # redirect_field_name = 'blog/post_detail.html'
    model =Post
    # def get_queryset(self):
    #     return Post.objects.all()
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['post-detail'] = Post.objects.all()
    #     return context
    # queryset = Post.objects.all()

class CreatePostView(LoginRequiredMixin, CreateView):
    login_url ='/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post
    # success_url = reverse_lazy('post_detail') #two

class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url ='/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post
    # success_url = reverse_lazy('post_detail') #one

    # class LoginUserView(auth_views.LoginView):
    # template_name = "blog/post_detail.html"
    # def get_success_url(self):
        # return self.get_redirect_url('post_detail')
        # if url:
        #     return url
        # elif self.request.user.is_superuser:
        # return reverse("post_detail")
        # else:
            # return reverse("profile")

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')

#################################################
#################################################
@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)



@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method =='POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk = post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment= get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect ('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk =post_pk)
