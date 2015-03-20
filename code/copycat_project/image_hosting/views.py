from django.shortcuts import render
from image_hosting.models import Category, Image
from django.http import HttpResponse

category_list = Category.objects.order_by('id')  # always pass all categories to every page


#  category_name must ether pro, funny or other
def index(request, category_name=0):
    context_dict = {'categories': category_list}

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
    return render(request, 'index.html', context_dict)


def upload(request):
    # TODO: after upload make it show the image in image view
    context_dict = {'categories': category_list, 'page_name': 'Image Upload'}

    if request.method == 'POST':
        if 'form' in request.POST:
            pass

    return render(request, 'upload.html', context_dict)


# Image View for single image page
def view(request, url_image_name):
    context_dict = {'categories': category_list, 'page_name': 'Image View'}

    try:
        context_dict['image'] = Image.objects.get(url_image_name=url_image_name)
    except Image.DoesNotExist:
        return index(request)

    return render(request, 'index.html', context_dict)

