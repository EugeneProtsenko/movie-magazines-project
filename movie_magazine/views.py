from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from movie_magazine.forms import MagazineForm, CriticCreationForm, CriticYearUpdateForm
from movie_magazine.models import Critic, Magazine, Topic


@login_required
def index(request):
    """View function for the home page of the site."""

    num_critics = Critic.objects.count()
    num_magazines = Magazine.objects.count()
    num_topics = Topic.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_critics": num_critics,
        "num_magazines": num_magazines,
        "num_topics": num_topics,
        "num_visits": num_visits + 1,
    }

    return render(request, "movie_magazine/index.html", context=context)


class TopicListView(LoginRequiredMixin, generic.ListView):
    model = Topic
    context_object_name = "topic_list"
    template_name = "movie_magazine/topic_list.html"
    paginate_by = 5


class TopicCreateView(LoginRequiredMixin, generic.CreateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("movie_magazine:topic-list")


class TopicUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("movie_magazine:topic-list")


class TopicDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Topic
    success_url = reverse_lazy("movie_magazine:topic-list")


class MagazineListView(LoginRequiredMixin, generic.ListView):
    model = Magazine
    queryset = Magazine.objects.select_related("topic")
    paginate_by = 5


class MagazineDetailView(LoginRequiredMixin, generic.DetailView):
    model = Magazine


class MagazineCreateView(LoginRequiredMixin, generic.CreateView):
    model = Magazine
    form_class = MagazineForm
    success_url = reverse_lazy("movie_magazine:magazine-list")


class MagazineUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Magazine
    form_class = MagazineForm
    success_url = reverse_lazy("movie_magazine:magazine-list")


class MagazineDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Magazine
    success_url = reverse_lazy("movie_magazine:magazine-list")


class CriticListView(LoginRequiredMixin, generic.ListView):
    model = Critic
    paginate_by = 5


class CriticDetailView(LoginRequiredMixin, generic.DetailView):
    model = Critic
    queryset = Critic.objects.all().prefetch_related("magazines__topic")


class CriticCreateView(LoginRequiredMixin, generic.CreateView):
    model = Critic
    form_class = CriticCreationForm


class CriticYearUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Critic
    form_class = CriticYearUpdateForm
    success_url = reverse_lazy("movie_magazine:critic-list")


class CriticDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Critic
    success_url = reverse_lazy("")


@login_required
def toggle_assign_to_magazine(request, pk):
    critic = Critic.objects.get(id=request.user.id)
    if (
        Magazine.objects.get(id=pk) in critic.magazines.all()
    ):
        critic.magazines.remove(pk)
    else:
        critic.magazines.add(pk)
    return HttpResponseRedirect(reverse_lazy("movie_magazine:magazine-detail", args=[pk]))