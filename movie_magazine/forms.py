from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from movie_magazine.models import Magazine, Critic


class MagazineForm(forms.ModelForm):
    critics = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Magazine
        fields = "__all__"


class CriticCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Critic
        fields = UserCreationForm.Meta.fields + (
            "years_of_experience",
            "first_name",
            "last_name",
        )

    def clean_years_of_experience(self):  # this logic is optional, but possible
        return validate_years_of_experience(self.cleaned_data["years_of_experience"])


class CriticYearUpdateForm(forms.ModelForm):
    class Meta:
        model = Critic
        fields = ["years_of_experience"]

    def clean_license_number(self):
        return validate_years_of_experience(self.cleaned_data["ears_of_experience"])


def validate_years_of_experience(
    years_of_experience,
):
    if years_of_experience < 0 or 100 < years_of_experience:
        raise ValidationError("Experience should be real")
    elif type(years_of_experience) != int:
        raise ValidationError("Must be a number")
    return years_of_experience
