from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = [
            "name",
        ]

    def __str__(self):
        return self.name


class Critic(AbstractUser):
    years_of_experience = models.IntegerField(default=0)

    class Meta:
        verbose_name = "critic"
        verbose_name_plural = "critics"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("movie_magazine:critic-detail", kwargs={"pk": self.pk})


class Magazine(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    critics = models.ManyToManyField(Critic, related_name="magazines")

    def __str__(self):
        return self.title
