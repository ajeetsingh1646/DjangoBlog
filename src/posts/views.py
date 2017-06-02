from urllib.parse import quote_plus
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.utils import timezone
# Create your views here.

def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "<a href='#'>Successfully Submited.</a>", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'form1': form,
    }
    return render(request, "post_form.html", context)

def post_detail(request,id):   # retreive
    inst = get_object_or_404(Post,id=id)
    if inst.draft:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404

    share_string = quote_plus(inst.content)
    context = {
        'title' : inst.title,
        'instance' : inst,
        'share_string': share_string
    }
    return render(request, "post_detail.html", context)

def post_list(request):     #List items
    today = timezone.now().date()
    queryset_list = Post.objects.active()
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(Q(title__icontains=query)|
                                             Q(content__icontains=query)|
                                             Q(user__first_name__icontains=query)|
                                             Q(user__last_name__icontains=query)
                                             ).distinct()
    paginator = Paginator(queryset_list, 5)  # Show 5 contacts per page
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        'object_list': queryset,
        'title': 'List.',
        'page_request_var': page_request_var,
        'today': today
    }
    return render(request, "post_list.html", context)


def post_update(request, id= None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    inst = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None ,instance = inst)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        #message success
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
            'title': inst.title,
            'instance': inst,
            'form1': form,
        }
    return render(request, "post_form.html", context)

def post_delete(request, id=None ):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, "Successfully deleted.")
    queryset = Post.objects.all()
    context = {
        'object_list': queryset,
        'title': 'List.'
    }
    return render(request, "base.html", context)
    #return redirect("posts: list")
