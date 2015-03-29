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

#After running the script dont forget to copy images from 'images' folder to your 'media/images/' folder

#professional category

    add_img(cat=pro_cat,
            caption="time is money ken",
            image="images/Lean_Legal_Professional_Firms.jpg",
            views=22,
            up_votes=55,
            down_votes=68,)
    
    add_img(cat=pro_cat,
            caption="ryan started the fire",
            image="images/fired_guy.jpg",
            views=33,
            up_votes=7,
            down_votes=999,)

    add_img(cat=pro_cat,
            caption="cool business chat",
            image="images/Growth_Business_Concept.jpg",
            views=44,
            up_votes=71,
            down_votes=978,)

    add_img(cat=pro_cat,
            caption="hand",
            image="images/hand.jpg",
            views=55,
            up_votes=58,
            down_votes=0,)
    
    add_img(cat=pro_cat,
            caption="Jigsaw falling into place",
            image="images/jigsaw.jpg",
            views=66,
            up_votes=18,
            down_votes=999,)

    add_img(cat=pro_cat,
            caption="office",
            image="images/keith1024.jpg",
            views=77,
            up_votes=19,
            down_votes=99,)

    add_img(cat=pro_cat,
            caption="10/10 innovation",
            image="images/orange.jpg",
            views=88,
            up_votes=995,
            down_votes=7,)
    
    add_img(cat=pro_cat,
            caption="shoot the runner",
            image="images/Runners.jpg",
            views=99,
            up_votes=16,
            down_votes=95,)

    add_img(cat=pro_cat,
            caption="cool bro",
            image="images/strat.jpg",
            views=110,
            up_votes=14,
            down_votes=95,)

    add_img(cat=pro_cat,
            caption="dairy",
            image="images/suit_up.jpg",
            views=110,
            up_votes=17,
            down_votes=8,)

#funny category

    add_img(cat=funny_cat,
            caption="drizzy",
            image="images/matching_sweaters.jpg",
            views=11,
            up_votes=41,
            down_votes=9,)

    add_img(cat=funny_cat,
            caption="drizzy",
            image="images/matching_sweaters.jpg",
            views=10,
            up_votes=71,
            down_votes=9,)

    add_img(cat=funny_cat,
            caption="drizzy",
            image="images/matching_sweaters.jpg",
            views=1,
            up_votes=1,
            down_votes=97,)

    add_img(cat=funny_cat,
            caption="the boy",
            image="images/drakeee.jpg",
            views=10,
            up_votes=51,
            down_votes=9,)

    add_img(cat=funny_cat,
            caption="dweeb",
            image="images/yolo.jpg",
            views=10,
            up_votes=1,
            down_votes=95,)

    add_img(cat=funny_cat,
            caption="...",
            image="images/tumblken.jpeg",
            views=10,
            up_votes=155,
            down_votes=9,)

    add_img(cat=funny_cat,
            caption="cattt",
            image="images/pew.jpg",
            views=0,
            up_votes=1,
            down_votes=96,)

    add_img(cat=funny_cat,
            caption="stache",
            image="images/Funny-meme3.jpg",
            views=10,
            up_votes=11,
            down_votes=9,)

    add_img(cat=funny_cat,
            caption="hai",
            image="images/meme.jpg",
            views=11,
            up_votes=1,
            down_votes=91,)

    add_img(cat=funny_cat,
            caption="office",
            image="images/scott2.jpg",
            views=11,
            up_votes=12,
            down_votes=9,)

    add_img(cat=funny_cat,
            caption="yo",
            image="images/scott1.jpg",
            views=112,
            up_votes=1,
            down_votes=92,)

    add_img(cat=funny_cat,
            caption="GTA V coming to PC soon :)",
            image="images/gta_v_pc.gif",
            views=200,
            up_votes=25,
            down_votes=3,)

#other category

    add_img(cat=other_cat,
            caption="why",
            image="images/otherrr.jpg",
            views=11,
            up_votes=4,
            down_votes=55,)

    add_img(cat=other_cat,
            caption="je suis",
            image="images/logo-google.png",
            views=4,
            up_votes=18,
            down_votes=9,)

    add_img(cat=other_cat,
            caption="pencil",
            image="images/others.png",
            views=5,
            up_votes=18,
            down_votes=9,)

    add_img(cat=other_cat,
            caption="dunno",
            image="images/strange.png",
            views=6,
            up_votes=15,
            down_votes=98,)

    add_img(cat=other_cat,
            caption="ugh",
            image="images/jooh.jpeg",
            views=140,
            up_votes=1,
            down_votes=955,)

    add_img(cat=other_cat,
            caption="scrambled like",
            image="images/egg.jpg",
            views=150,
            up_votes=1,
            down_votes=9,)

    add_img(cat=other_cat,
            caption="listen",
            image="images/WalkmenEveryone.jpg",
            views=1150,
            up_votes=4,
            down_votes=9,)

    add_img(cat=other_cat,
            caption="listenn",
            image="images/gallus.jpg",
            views=150,
            up_votes=44,
            down_votes=9,)

    add_img(cat=other_cat,
            caption="listennn",
            image="images/flume.jpg",
            views=180,
            up_votes=1,
            down_votes=44,)

    add_img(cat=other_cat,
            caption="know",
            image="images/Ken_Logo.jpg",
            views=30,
            up_votes=4,
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
