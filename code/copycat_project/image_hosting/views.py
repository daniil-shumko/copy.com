from django.shortcuts import render
from image_hosting.models import Category, Image
import random
from image_hosting.forms import UploadForm
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


#  category_name must ether pro, funny or other
def index(request, category_name=0):
    context_dict = {}
    context_dict['all_votes'] = get_all_voted_images(request)

    # TODO: make ajax so you can show more images when page scrols to the end
    image_list = ''
    try:
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
            context_dict['page_name'] = 'Home | Most Popular'

    except Category.DoesNotExist:
        pass

    context_dict['images'] = split_images(image_list)
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
    context_dict = {'page_name': 'Image View', 'all_votes': get_all_voted_images(request)}

    try:
        image = Image.objects.get(image=image_name)
        image.views += 1
        image.save()
        context_dict['image'] = image

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
        image_name = Image.objects.get(id=rnd).image.name
    except Image.DoesNotExist:
        return index(request)

    return view_image(request, image_name)


def vote_image(request):
    image_id = None
    value = None
    votes = ''
    if request.method == 'GET':
        image_id = request.GET['image_id']
        value = request.GET['vote']

    previous_votes = request.session.get('all_votes')
    if not previous_votes:
        previous_votes = []

    if image_id in previous_votes:
        votes = 'already_voted'
    else:
        if image_id:
            image = Image.objects.get(id=image_id)
            if image:
                if value == 'up':
                    image.up_votes += 1
                    previous_votes.append(image_id)
                    votes = str(image.up_votes) + "/" + str(image.down_votes)
                elif value == 'down':
                    image.down_votes += 1
                    previous_votes.append(image_id)
                    votes = str(image.up_votes) + "/" + str(image.down_votes)
                image.save()

    request.session['all_votes'] = previous_votes

    return HttpResponse(votes)


def split_images(images):
    chunk = []
    chunks = []
    n = 2  # changing this number will make images to display in multiple colums on the index page

    for x in range(0, len(images), n):
        # Extract n elements
        chunk = images[x:x + n]
        # Add them to list
        chunks.append(chunk)

    # Return the new list
    return chunks


def get_all_voted_images(request):
    previous_votes = request.session.get('all_votes')
    if not previous_votes:
        previous_votes = []
    else:
        previous_votes = map(int, previous_votes)

    return previous_votes


@csrf_exempt
def api(request):
    cats = Category.objects.all()
    all_cat_ids = []
    result_dict = {'success': 'false', 'error': 'Unknown'}

    for cat in cats:
        all_cat_ids.append(cat.id)

    if request.method == 'POST':
        data = request.POST

        if data['category'].isdigit() and (int(data['category']) in all_cat_ids):
            if len(data['caption']) <= 128:
                if not request.FILES:
                    result_dict['error'] = 'No image file in POST'
                    return JsonResponse(result_dict)
                else:
                    form = UploadForm(data, request.FILES)
                    category = Category.objects.get(id=data['category'])

                    if category:
                        image = form.save(commit=False)
                        image.views = 0
                        image.up_votes = 0
                        image.down_votes = 0
                        image.save()

                        del result_dict['error']
                        result_dict['success'] = 'true'
                        result_dict['image_url'] = 'http://daniilshumko.pythonanywhere.com/media/'+image.image.name
                        result_dict['caption'] = image.caption
                        result_dict['category'] = image.category.name
                        return JsonResponse(result_dict)
                    else:
                        result_dict['error'] = 'Category with that ID does not exist'
                        return JsonResponse(result_dict)

            else:
                result_dict['error'] = 'Caption too long'
                return JsonResponse(result_dict)
        else:
            result_dict['error'] = 'Error wrong category id'
            return JsonResponse(result_dict)
    else:
        context_dict = {'categories': cats}
        return render(request, 'image_hosting/api.html', context_dict)


def remove_image(request, image_name):
    if request.user.is_authenticated():  #TODO: redirect to 404 if admin not loged in
        try:
            image = Image.objects.get(image=image_name)
            image.delete()
            print "Image REMOVED: "+image_name
        except Image.DoesNotExist:
            print("Image does not exist")
            return index(request)

    return index(request)


def test(request):
    return render(request, 'api_test/test.html')