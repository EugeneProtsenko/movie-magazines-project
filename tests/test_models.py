from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from movie_magazine.models import Topic, Magazine


class ModelTests(TestCase):
    def test_topic_str(self):
        topic = Topic.objects.create(name="test")
        self.assertEqual(str(topic), str(topic.name))

    def test_create_critic_with_years_of_experience(self):
        username = "test"
        password = "test123"
        years_of_experience = 8
        critic = get_user_model().objects.create_user(
            username=username,
            password=password,
            years_of_experience=years_of_experience,
        )
        self.assertEqual(critic.username, username)
        self.assertEqual(critic.years_of_experience, years_of_experience)
        self.assertTrue(critic.check_password(password))

    def test_magazine_str(self):
        topic = Topic.objects.create(name="test")
        magazine = Magazine.objects.create(
            title="test", content="test123", published_date="2001-09-07", topic=topic
        )
        self.assertEqual(str(magazine), magazine.title)


class CriticModelTest(TestCase):
    def setUp(self):
        self.critic = get_user_model().objects.create_user(
            username="testcritic", password="12345", years_of_experience=9
        )

    def test_get_absolute_url(self):
        expected_url = reverse(
            "movie_magazine:critic-detail", kwargs={"pk": self.critic.pk}
        )
        actual_url = self.critic.get_absolute_url()
        self.assertEqual(expected_url, actual_url)
