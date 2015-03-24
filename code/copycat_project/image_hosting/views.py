from django.shortcuts import render
from image_hosting.models import Category, Image
import random
from image_hosting.forms import UploadForm
from django.http import HttpResponse


#  category_name must ether pro, funny or other
def index(request, category_name=0):
    context_dict = {}

    # TODO: make ajax so you can show more images when page scrols to the end
    image_list = ''

    try:
        #  category = Category.objects.get(slug=category_name_slug)
        if category_name == 'pro':
            category = Category.objects.get(name='Professional')
            image_list = Image.objects.filter(category=category)
            context_dict['page_name'] = 'Professional'
        elif category_name == 'funny':
            category = Category.objects.get(name='Funny')
            image_list = Image.objects.filter(category=category)
            context_dict['page_name'] = 'Funny'
        elif category_name == 'other':
            category = Category.objects.get(name='Other')
            image_list = Image.objects.filter(category=category)
            context_dict['page_name'] = 'Other'
        elif category_name == 'up':
            image_list = Image.objects.order_by('-up_votes')
            context_dict['page_name'] = 'Most Up Voted'
        elif category_name == 'down':
            image_list = Image.objects.order_by('-down_votes')
            context_dict['page_name'] = 'Most Down Voted'
        elif category_name == 'recent':
            image_list = Image.objects.order_by('-timestamp')
            context_dict['page_name'] = 'Most Recent'
        else:  # category_name == 'popular':
            image_list = Image.objects.order_by('-views', '-up_votes')
            context_dict['page_name'] = 'Most Popular'

    except Category.DoesNotExist:
        pass

    context_dict['images'] = image_list
    return render(request, 'image_hosting/index.html', context_dict)


def upload(request):
    context_dict = {'page_name': 'Image Upload'}

    # if request.method == 'POST':
    # if 'form' in request.POST:
    #         pass

    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            form.clean_image()

            image = form.save(commit=False)
            image.views = 0
            image.up_votes = 0
            image.down_votes = 0
            image.save()
            # probably better to use a redirect here.

            return view_image(request, image.image.name)
        else:
            print form.errors
    else:
        form = UploadForm()

    context_dict['form'] = form

    return render(request, 'image_hosting/upload.html', context_dict)


# Image View for single image page. Thsi take image name without "images/"
def view_image(request, image_name):
    context_dict = {'page_name': 'Image View'}
    try:
        context_dict['image'] = Image.objects.get(image=image_name)
    except Image.DoesNotExist:
        return index(request)

    return render(request, 'image_hosting/image_view.html', context_dict)


def cat_pro(request):
    return index(request, 'pro')


def cat_funny(request):
    return index(request, 'funny')


def cat_other(request):
    return index(request, 'other')


def cat_up(request):
    return index(request, 'up')


def cat_down(request):
    return index(request, 'down')


def cat_recent(request):
    return index(request, 'recent')


def random_image(request):
    try:
        count = Image.objects.count()
        rnd = random.randint(1, count)
        print rnd
        image_name = Image.objects.get(id=rnd).image.name
    except Image.DoesNotExist:
        return index(request)

    return view_image(request, image_name)


