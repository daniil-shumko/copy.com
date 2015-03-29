from django.shortcuts import render
from image_hosting.models import Category, Image
import random
from image_hosting.forms import UploadForm
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


#  Index page displays images in a grid. Index view is used to diplay images by categories, just give it a category name.
def index(request, category_name=0):
    context_dict = {}
    context_dict['all_votes'] = get_all_voted_images(request)

    # TODO: make ajax so you can show more images when page scrolls to the end. (this will never happen :))
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


# Image View for single image page. This take image name and location in media folder. Example "images/image.jpg"
# also adds +1 to views for the image
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


#  this just calls index view with category name 'pro' which is Professional category
def cat_pro(request):
    return index(request, 'pro')


#  this just calls index view with category name 'funny' which is Funny category
def cat_funny(request):
    return index(request, 'funny')


#  this just calls index view with category name 'other' which is Other category
def cat_other(request):
    return index(request, 'other')


#  this just calls index view with category name 'up' which is Most Up Voted images
def cat_up(request):
    return index(request, 'up')


#  this just calls index view with category name 'down' which is Most Down Voted images
def cat_down(request):
    return index(request, 'down')


#  this just calls index view with category name 'recent' which is Most Recent images
def cat_recent(request):
    return index(request, 'recent')


# gets a random image from database and call view_image view with the image name to be displayed
def random_image(request):
    try:
        all_images = Image.objects.all()
        count = all_images.count()
        rnd = random.randint(0, count)
        image_name = all_images[rnd].image.name
    except Image.DoesNotExist:
        return index(request)

    return view_image(request, image_name)


#  this is called by AJAX and gets image id and type of vote from GET request
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


#  this is used to split a list of images into groups of two to display images in a grid on the index page and category pages
def split_images(images):
    chunk = []
    chunks = []
    n = 2  # changing this number will allow images to display in multiple columns on the index page(html will need to be adjusted)

    for x in range(0, len(images), n):
        # Extract n elements
        chunk = images[x:x + n]
        # Add them to list
        chunks.append(chunk)

    # Return the new list
    return chunks


#  gets a list of images ids that user has voted for. This is stored on server using session cookie
def get_all_voted_images(request):
    previous_votes = request.session.get('all_votes')
    if not previous_votes:
        previous_votes = []
    else:
        previous_votes = map(int, previous_votes)

    return previous_votes


#  api that return a html page if no POST request been received. Otherwise checks the POST request
# and uploads an image to the database and responses with JSON
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
                        result_dict['image_url'] = 'http://copycatd7.pythonanywhere.com/media/'+image.image.name
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


#  this feature is strictly for admins only. If you login using '/admin/' link you will see a 'REMOVE IMAGE'
# link under every image which calls this function and allows you to remove the image from the database
def remove_image(request, image_name):
    if request.user.is_authenticated():
        try:
            image = Image.objects.get(image=image_name)
            image.delete()
            print "Image REMOVED: "+image_name
        except Image.DoesNotExist:
            print("Image does not exist")
            return index(request)
    else:
        return error404(request)
    return index(request)


#  test for the API. for demo only!
def test(request):
    return render(request, 'api_test/test.html')


#  When error 404 occurs this function is called. This gets a random image from 'Funny' category and displays Image View
# page with error message
def error404(request):
    context_dict = {'all_votes': get_all_voted_images(request)}
    category = Category.objects.get(name='Funny')
    image_list = Image.objects.filter(category=category)
    count_images = image_list.count()
    rnd = random.randint(0, count_images)
    context_dict['image'] = image_list[rnd]

    return render(request, 'image_hosting/404.html', context_dict)