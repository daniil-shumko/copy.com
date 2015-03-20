__author__ = 'Daniil'

import os
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'copycat_project.settings')

import django

django.setup()

from image_hosting.models import Category, Image


def populate():
    pro_cat = get_cat("Professional")
    funny_cat = get_cat("Funny")
    other_cat = get_cat("Other")

    # funny category
    add_img(cat=funny_cat,
            caption="Funny cat pic",
            url_image_name="sdfgwfsd.jpg",)

    add_img(cat=funny_cat,
            caption="Arbuz",
            url_image_name="qweasdf1.jpg",
            views=5,)

    add_img(cat=funny_cat,
            caption="Hey elephant",
            url_image_name="elephant213.jpg",
            views=20,
            up_votes=10,)

    add_img(cat=funny_cat,
            caption="My humps",
            url_image_name="131afsd.jpg",
            views=50,
            down_votes=10,)

    add_img(cat=funny_cat,
            caption="Craqzy dog",
            url_image_name="dog.jpg",)

    # pro category
    add_img(cat=pro_cat,
            caption="My PC",
            url_image_name="pcworks_1.jpg",
            views=5,
            up_votes=1,)

    add_img(cat=pro_cat,
            caption="Computer science",
            url_image_name="pcworks.jpg",
            views=90,
            up_votes=10,
            down_votes=30,)

    add_img(cat=pro_cat,
            caption="No",
            url_image_name="nonono.jpg",)

    # other category
    add_img(cat=other_cat,
            caption="Some other stuff",
            url_image_name="otherpics.jpg",
            views=11,
            up_votes=1,
            down_votes=9,)

    # Print out what we have added to the database.
    for c in Category.objects.all():
        for i in Image.objects.filter(category=c):
            print "- {0} - {1}".format(str(c), str(i))


def add_img(cat, caption, url_image_name, views=0, up_votes=0, down_votes=0):
    img = Image.objects.get_or_create(category=cat, url_image_name=url_image_name)[0]
    img.caption = caption
    img.views = views
    img.up_votes = up_votes
    img.down_votes = down_votes

    img.save()
    return img


# get cathegory becaseu we only have 3 and wont be adding more
def get_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    return c

# Start execution here!
if __name__ == '__main__':
    print "Starting Image population script..."
    populate()