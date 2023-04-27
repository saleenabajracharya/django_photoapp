from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from django.urls import reverse 
from .models import Post
# from serializer import post_serializer

# Create your tests here.
class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@email.com",
            password="secret"
        )

        cls.post = Post.objects.create(
            title = "title",
            image = "image",
            author = cls.user,
        )
    def test_get_queryset_authenticated_user(self):
        url= reverse('blog-home')
        response=self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        # serializer_data=post_serializer([self.post],many=True)
        # self.assertEqual(response.data,serializer_data)

    def test_post_model(self):
        self.assertEqual(self.post.title,"title")
        # self.assertEqual(self.post.body,"Content")
        self.assertEqual(self.post.author.username,"testuser")
        self.assertEqual(str(self.post),"title")
        self.assertEqual(self.post.get_absolute_url(),"/post/1/")

    def test_url_exists_at_correct_location_listview(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code,302)

    def test_url_exists_at_correct_location_detailview(self):
        response = self.client.get("/post/1/")
        self.assertEqual(response.status_code,302)

    def test_url_exists_at_correct_location_detailview(self):
        url= reverse('blog-home')
        response = self.client.get(url)
        self.assertEqual(response.status_code,302)

    def test_url_exists_at_correct_location_detailview(self):
        url= reverse('search')
        response = self.client.get(url)
        self.assertEqual(response.status_code,302)

    def test_url_exists_at_correct_location_detailview(self):
        url= reverse('blog-about')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)

    # def test_post_listview(self):
    #     response =self.client.get(reverse("blog-home"))
    #     self.assertEqual(response.status_code,200)
    #     self.assertContains(response,"Title")
    #     self.assertTemplateUsed(response,"blog-home.html")

    # # def test_post_detailview(self):
    # #     response = self.client.get(reverse("blog-detail",
    # #                                        kwargs={"pk":self.post.pk}))
       
    #     self.assertEqual(response.status_code,200)
    #     no_response = self.client.get("/post/100000/")
    #     self.assertEqual(no_response.status_code,302)
    #     self.assertContains(response,"title")
    #     self.assertTemplateUsed(response,"post_detail.html")

    def test_post_updateview(self):
        response = self.client.post(
            reverse("blog-update",args="1"),
            {
                "title":"title",
                "image":"image",
            },
        )
        self.assertEqual(response.status_code,302)
        self.assertEqual(Post.objects.last().title,"title")
        self.assertEqual(Post.objects.last().image,"image")


    def test_post_deleteview(self):
        response = self.client.post(reverse("blog-delete",args="1"))
        self.assertEqual(response.status_code,302)



 