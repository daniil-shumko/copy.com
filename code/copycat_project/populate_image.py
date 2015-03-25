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

#TODO: update with new data

    add_img(cat=pro_cat,
            caption="Computer",
            image="images/image_name_opQYZHv.png",
            views=11,
            up_votes=1,
            down_votes=9,)

    # Print out what we have added to the database.
    for c in Category.objects.all():
        for i in Image.objects.filter(category=c):
            print "- {0} - {1}".format(str(c), str(i))


def add_img(cat, caption, image, views=0, up_votes=0, down_votes=0):
    img = Image.objects.get_or_create(category=cat, image=image)[0]
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