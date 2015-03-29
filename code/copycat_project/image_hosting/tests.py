from django.test import TestCase
from django.core.urlresolvers import reverse
from image_hosting.models import Category, Image


class CategoryMethodTests(TestCase):
    def test_ensure_views_are_positive(self):
        cat = Category(name='test')
        cat.save()
        self.assertEqual((cat.name == 'test'), True)


class ImageMethodTests(TestCase):
    def test_ensure_caption_is_set(self):
        cat = Category(name='test2')
        cat.save()
        image = Image(category=cat)
        image.caption = 'test caption'
        image.save()
        self.assertEqual((image.caption == 'test caption'), True)

    def test_ensure_image_is_set(self):
        cat = Category(name='test3')
        cat.save()
        image = Image(category=cat)
        image.image = 'images/img.jpg'
        image.save()
        self.assertEqual((image.image == 'images/img.jpg'), True)

    def test_ensure_views_are_set(self):
        cat = Category(name='test4')
        cat.save()
        image = Image(category=cat)
        image.views = 12
        image.save()
        self.assertEqual((image.views == 12), True)

    def test_ensure_upvotes_are_set(self):
        cat = Category(name='test5')
        cat.save()
        image = Image(category=cat)
        image.up_votes = 9
        image.save()
        self.assertEqual((image.up_votes == 9), True)

    def test_ensure_downvotes_are_set(self):
        cat = Category(name='test6')
        cat.save()
        image = Image(category=cat)
        image.down_votes = 11
        image.save()
        self.assertEqual((image.down_votes == 11), True)

class IndexViewTests(TestCase):

    def test_index_view_with_no_images(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no image present.")
        self.assertQuerysetEqual(response.context['images'], [])

class UploadViewTests(TestCase):
    def test_upload_view(self):
        response = self.client.get(reverse('upload'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Image Upload")

        self.assertQuerysetEqual(response.context['page_name'], [])