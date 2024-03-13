from django.test import TestCase

from movie_magazine.forms import (
    CriticCreationForm,
    CriticYearUpdateForm,
    CriticSearchForm,
)
from movie_magazine.models import Critic


class CriticCreationFormTest(TestCase):
    def test_critic_creation_form_is_valid(self):
        form_data = {
            "username": "test",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "years_of_experience": 7,
            "first_name": "Test first",
            "last_name": "Test last",
        }
        form = CriticCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class CriticYearUpdateFormTest(TestCase):
    def setUp(self):
        self.critic = Critic.objects.create_user(
            username="testcritic", password="12345", years_of_experience=8
        )

    def test_form_critic_update_is_valid(self):
        form = CriticYearUpdateForm(
            instance=self.critic, data={"years_of_experience": 8}
        )
        self.assertTrue(form.is_valid())


class CriticSearchFormTest(TestCase):
    def test_model_field_present(self):
        field = "username"
        form_data = {field: "test_model"}
        form = CriticSearchForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertTrue(field in form.fields)
