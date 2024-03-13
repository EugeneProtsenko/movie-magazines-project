from django.urls import path

from movie_magazine.views import (
    index,
    TopicListView,
    TopicCreateView,
    TopicUpdateView,
    TopicDeleteView,
    MagazineListView,
    MagazineDetailView,
    MagazineCreateView,
    MagazineUpdateView,
    MagazineDeleteView,
    CriticListView,
    CriticDetailView,
    CriticCreateView,
    CriticYearUpdateView,
    CriticDeleteView,
    toggle_assign_to_magazine,
)


urlpatterns = [
    path("", index, name="index"),
    path("topics/", TopicListView.as_view(), name="topic-list"),
    path("topics/create/", TopicCreateView.as_view(), name="topic-create"),
    path("topics/<int:pk>/update/", TopicUpdateView.as_view(), name="topic-update"),
    path("topics/<int:pk>/delete/", TopicDeleteView.as_view(), name="topic-delete"),
    path("magazines/", MagazineListView.as_view(), name="magazine-list"),
    path("magazines/<int:pk>/", MagazineDetailView.as_view(), name="magazine-detail"),
    path("magazines/create/", MagazineCreateView.as_view(), name="magazine-create"),
    path(
        "magazines/<int:pk>/update/",
        MagazineUpdateView.as_view(),
        name="magazine-update",
    ),
    path(
        "magazines/<int:pk>/delete/",
        MagazineDeleteView.as_view(),
        name="magazine-delete",
    ),
    path(
        "magazines/<int:pk>/toggle-assign/",
        toggle_assign_to_magazine,
        name="toggle-magazine-assign",
    ),
    path("critics/", CriticListView.as_view(), name="critic-list"),
    path("critics/<int:pk>/", CriticDetailView.as_view(), name="critic-detail"),
    path("critics/create/", CriticCreateView.as_view(), name="critic-create"),
    path(
        "critics/<int:pk>/update/",
        CriticYearUpdateView.as_view(),
        name="critic-update",
    ),
    path(
        "critics/<int:pk>/delete/",
        CriticDeleteView.as_view(),
        name="critic-delete",
    ),
]

app_name = "movie_magazine"
