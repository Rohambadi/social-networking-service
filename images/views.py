from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from .forms import ImagePostForm, ImageCreateForm, ComImagePostForm
from django.contrib import messages
from .models import Image
from django.conf import settings
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from common.decorators import ajax_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from actions.utils import create_action


@login_required
def image_post(request):
    if request.method == 'POST':
        form = ImagePostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            create_action(request.user, 'posted image', new_item)
            messages.success(request, 'Image add successfully!')
            return redirect(new_item.get_absolute_url())
            # return redirect('images:compost')
        else:
            messages.error(request, 'image add unsuccessfully!')
            return HttpResponse('image add unsuccessfully!')

    else:
        post_form = ImagePostForm()
        return render(request, 'images/image/post.html', {'post_form': post_form})


'''def com_image_post(request):
    if request.method == 'POST':
        photo_form = ImagePostForm(instance=request.user,
                                   data=request.POST, 
                                   files=request.FILES)
        desc_form = ComImagePostForm(instance=request.user,
                                     data=request.POST,
                                     files=request.FILES)
        if photo_form.is_valid() and desc_form.is_valid():
            new_detail= photo_form.save(commit=False)
            desc_form.save(commit=False)
            new_detail.set_title(desc_form.cleaned_data['title'])
            new_detail.set_description(desc_form.cleaned_data['description'])
            new_detail.save()
            messages.success(request, " your post add successfully!")
            return redirect(new_detail.get_absolute_url())
        else:
            messages.error(request, "your post add failed!")
            return HttpResponse('our post add failed!')

    else:
        photo_form = ImagePostForm(instance=request.GET)
        desc_form = ComImagePostForm()
        return render(request, 'images/image/edit.html', {'photo_form': photo_form, 'desc_form': desc_form})'''


@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            create_action(request.user, 'bookmarked image', new_item)
            messages.success(request, 'Image add successfully!')
            return redirect(new_item.get_absolute_url())

    else:
        form = ImageCreateForm(data=request.GET)
        return render(request, 'images/image/create.html', {'section': 'images', 'form': form})


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, 'images/image/detail.html', {'section': 'images', 'image': image})


@ajax_required
@login_required
@require_POST
def image_like(request):
    # if not request.is_ajax():
        # return HttpResponseBadRequest()
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'error'})


@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 10)
    page = request.GET.get("page")
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'images/image/list_ajax.html',
                      {'section': 'images', 'images': images})
    return render(request, 'images/image/list.html',
                  {'section': 'images', 'images': images})