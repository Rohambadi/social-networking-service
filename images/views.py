from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ImagePostForm
from django.contrib import messages
from .models import Image


@login_required()
def image_post(request):
    '''if request.method == 'POST':
        post_form = ImagePostForm(request.POST)
        if post_form.is_valid():
            cd = post_form.cleaned_data
            #image = cd['image']
            new_post = post_form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'Image add successfully!')
            # return HttpResponse('Image add successfully!')
            return render(request, 'images/image/detail.html', {'image': image})

    else:
        post_form = ImagePostForm()
        return render(request, 'images/image/post.html', {'post_form': post_form}) '''
    if request.method != 'POST':
        post_form = ImagePostForm()
    else:
        post_form = ImagePostForm(data=request.POST)
        if post_form.is_valid():
            cd = post_form.cleaned_data
            new_form= post_form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            return redirect('images:image_detail')
        else:
            return HttpResponse('Image add unsuccessfully!')
    context = {'post_form': post_form}
    return render(request, 'images/image/post.html', context)


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, '/images/image/detail.html', {'section': 'images', 'image': image})
