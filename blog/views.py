from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
# Create your views here.
from .models import Post,Comment
from .forms import EmailPostForm, CommentForm, SearchForm
from taggit.models import Tag
from django.db.models import Count



########################VIEWS##########################

"""
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

"""

def post_list(request,tag_slug=None):
    object_list = Post.published.all()
    tag = None
    count = 5
    home = True
    form = SearchForm()
    all_tags = Tag.objects.all()
    most_commented_posts = Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list,3)
    page = request.GET.get('page')

    try:
        #contacts = paginator.get_page(page)
        posts = paginator.get_page(page)
    except PageNotAnInteger:
        posts = paginator.page(1) # deliver first page posts when page is not integer
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request , 'blog/post/list.html' , {'form':form,'home':home,'posts':posts,'tag':tag , 'page':page , 'most_commented_posts':most_commented_posts , 'all_tags':all_tags})


def post_detail(request , year=None , month=None , day=None , post=None):
    post = get_object_or_404(Post , status='published' , publish__year=year, publish__month = month, publish__day=day ,slug=post)
    comments = post.comments.filter(active=True)
    comments_count = post.comments.count()
    all_tags = Tag.objects.all()
    count = 5
    form = SearchForm()
    most_commented_posts = Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
        new_comment = False

    post_tags_ids = post.tags.values_list('id' , flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    return render(request , 'blog/post/detail.html' , {'post':post,'comments':comments,'comment_form':comment_form,'similar_posts':similar_posts  , 'most_commented_posts':most_commented_posts,'comments_count':comments_count,'all_tags':all_tags,'form':form})


def post_share(request , post_id):
    post = get_object_or_404(Post, id=post_id , status='published')
    count = 5
    most_commented_posts = Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
    sent = False
    to = None
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'],cd['email'],post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title , post_url , cd['name'] , cd['comments'])
            send_mail(subject,message,'my.blog.project.mailer@gmail.com',[cd['to']],fail_silently=False)
            sent=True
            to = cd['to']
            
    else:
            form = EmailPostForm()

    return render(request , 'blog/post/share.html' , {'post':post,'form':form,'sent':sent,'to':to  , 'most_commented_posts':most_commented_posts})

def post_search(request):
    form = SearchForm()
    cd = None
    results = None
    total_results = None
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            results = Post.published.filter(title__icontains=request.GET['query'])
            total_results = results.count()
    return render(request, 'blog/post/search.html' , {'cd':cd,'form':form,'results':results,'total_results':total_results})
