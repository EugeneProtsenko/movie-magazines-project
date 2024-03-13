from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="Test@Admin",
        )
        self.client.force_login(self.admin_user)
        self.critic = get_user_model().objects.create_user(
            username="author",
            password="Test@Author",
            years_of_experience=8,
        )

    def test_critic_years_of_experience_listed(self):
        url = reverse("admin:movie_magazine_critic_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.critic.years_of_experience)

    def test_critic_detail_years_of_experience_listed(self):
        url = reverse("admin:movie_magazine_critic_change", args=[self.critic.id])
        res = self.client.get(url)

        self.assertContains(res, self.critic.years_of_experience)
