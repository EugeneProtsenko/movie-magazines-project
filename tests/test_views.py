from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from movie_magazine.models import Topic, Critic, Magazine

TOPICS_URL = reverse("movie_magazine:topic-list")
MAGAZINES_URL = reverse("movie_magazine:magazine-list")
CRITICS_URL = reverse("movie_magazine:critic-list")


class PublicTopicTests(TestCase):
    def test_login_required(self):
        response = self.client.get(TOPICS_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateTopicTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1111",
        )
        self.client.force_login(self.user)

    def test_retrieve_topic_list(self):
        Topic.objects.create(name="test_name1")
        Topic.objects.create(name="test_name2")

        response = self.client.get(TOPICS_URL)

        topics = Topic.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["topic_list"]), list(topics))
        self.assertTemplateUsed(response, "movie_magazine/topic_list.html")

    def test_topic_list_search(self):
        Topic.objects.create(name="test_name")
        Topic.objects.create(name="Drama")
        response = self.client.get(TOPICS_URL, {"name": "test_name"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["topic_list"]),
            list(Topic.objects.filter(name="test_name")),
        )


class PublicMagazineTests(TestCase):
    def test_login_required(self):
        response = self.client.get(MAGAZINES_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateMagazineTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1111",
        )
        self.client.force_login(self.user)

    def test_retrieve_magazine_list(self):
        topic = Topic.objects.create(name="test_name")
        magazine1 = Magazine.objects.create(
            title="test1", content="test123", published_date="2020-05-02", topic=topic
        )
        magazine2 = Magazine.objects.create(
            title="test2",
            content="test123342",
            published_date="2021-05-02",
            topic=topic,
        )
        magazine1.critics.add(self.user)
        magazine2.critics.add(self.user)
        response = self.client.get(MAGAZINES_URL)
        magazines = Magazine.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["magazine_list"]), list(magazines))
        self.assertTemplateUsed(response, "movie_magazine/magazine_list.html")

    def test_magazine_list_search(self):
        topic = Topic.objects.create(
            name="test_name",
        )
        topic2 = Topic.objects.create(
            name="test_name2",
        )
        Magazine.objects.create(
            title="test12",
            content="test12312",
            published_date="2021-05-02",
            topic=topic,
        )
        Magazine.objects.create(
            title="new test",
            content="test1231sdfd2",
            published_date="2012-05-02",
            topic=topic2,
        )
        response = self.client.get(MAGAZINES_URL, {"title": "test_title"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["magazine_list"]),
            list(Magazine.objects.filter(title="test_title")),
        )


class PrivateCriticTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1111",
        )
        self.client.force_login(self.user)

    def test_create_critic(self):
        form_data = {
            "username": "test_username",
            "password1": "testpassword1234",
            "password2": "testpassword1234",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "years_of_experience": 3,
        }
        self.client.post(reverse("movie_magazine:critic-create"), data=form_data)
        user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(user.first_name, form_data["first_name"])
        self.assertEqual(user.last_name, form_data["last_name"])
        self.assertEqual(user.years_of_experience, form_data["years_of_experience"])

    def test_critic_search(self):
        Critic.objects.create(
            username="test_driver1", password="passowrd12345", years_of_experience=10
        )
        Critic.objects.create(
            username="test_driver2", password="passowrd12342", years_of_experience=11
        )
        response = self.client.get(CRITICS_URL, {"username": "critic"})
        critics = Critic.objects.filter(username__icontains="critic")
        self.assertEqual(list(response.context["critic_list"]), list(critics))
