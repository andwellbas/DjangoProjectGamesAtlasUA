from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator
from .models import News, FutureReleases, TopGames
from .forms import GameRatingForm, CommentForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Avg
from .models import GameRating
from django.db.models import F
from .forms import SignUpForm
from django.views import View
from . import price_parser


class MainPageView(View):
    template_name = "games_hub/main_page.html"

    def get(self, request):
        news_list = News.objects.all().order_by("-id")
        paginator = Paginator(news_list, 12)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            "news": page_obj,
        }
        return render(request, self.template_name, context)


class DetailNewsView(DetailView):
    template_name = "games_hub/detail_news_page.html"
    model = News
    context_object_name = "news"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        context["comments"] = self.get_object().comments.order_by("-created_date")
        return context

    def post(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.news = self.get_object()
            comment.save()

        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


# Check whether the value has been set "g-recaptcha-response".
def verify_recaptcha(response):
    return bool(response)


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            captcha = request.POST.get("g-recaptcha-response")
            if captcha:
                if verify_recaptcha(captcha):
                    email = form.cleaned_data["email"]
                    if User.objects.filter(email=email).exists():
                        form.add_error("email", "Аккаунт з такою поштою вже зареєстрований.")
                    else:
                        user = form.save(commit=False)
                        user.save()
                        login(request, user)
                        return redirect("starting-page")
                else:
                    form.add_error(None, "Неправильна перевірка reCAPTCHA.")
            else:
                form.add_error(None, "Будь ласка, заповніть поле reCAPTCHA.")
    else:
        form = SignUpForm()
    return render(request, "games_hub/register_page.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("starting-page")
        else:
            messages.error(request, "Неправильне ім'я користувача або пароль.")
    return render(request, "games_hub/login_page.html")


def logout_view(request):
    logout(request)
    messages.success(request, "Ви успішно вийшли з акаунту.")
    return redirect("login")


def price_comparison(request):
    return render(request, "games_hub/price_comparison.html")


def price_comparison_results(request):
    game_name = request.GET.get("game_name")

    steam = price_parser.get_steam_price(game_name)
    gamers_gate = price_parser.get_gamers_gate_price(game_name)
    games_planet = price_parser.get_games_planet_price(game_name)
    yu_play = price_parser.get_games_yu_play_price(game_name)
    win_game = price_parser.get_win_game_store_price(game_name)
    all_key_shop = price_parser.get_all_key_shop_price(game_name)
    noctre = price_parser.get_noctre_price(game_name)

    return render(request, "games_hub/price_comparison_result.html", {
        #  game_name
        "game_name": game_name,
        #  prices 0element in tuple
        "steam_price": steam[0],
        "gamers_gate_price": gamers_gate[0],
        "games_planet_price": games_planet[0],
        "yu_play_price": yu_play[0],
        "win_game_price": win_game[0],
        "alkey_price": all_key_shop[0],
        "noctre_price": noctre[0],
        #  links 1element in tuple
        "steam_link": steam[1],
        "gamers_gate_link": gamers_gate[1],
        "games_planet_link": games_planet[1],
        "yu_play_link": yu_play[1],
        "win_game_link": win_game[1],
        "alkey_link": all_key_shop[1],
        "noctre_link": noctre[1],
    })


class FutureReleasesPageView(ListView):
    template_name = "games_hub/future_releases_page.html"
    model = FutureReleases
    ordering = [F("release_date").asc(nulls_last=True)]
    context_object_name = "games"


class DetailFutureReleasesPageView(DetailView):
    template_name = "games_hub/detail_future_releases.html"
    model = FutureReleases
    context_object_name = "game"


@login_required
def vote_for_game(request, slug):
    game = get_object_or_404(FutureReleases, slug=slug)
    user = request.user

    if user not in game.voters.all():
        game.voters.add(user)
        game.save()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class TopGamesPageView(ListView):
    template_name = "games_hub/top_games_page.html"
    model = TopGames
    context_object_name = "games"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(avg_rating=Avg("game_ratings__rating")).order_by("-avg_rating").distinct()
        return queryset


class DetailTopGamesPageView(DetailView):
    model = TopGames
    template_name = "games_hub/detail_top_games_page.html"
    context_object_name = "game"

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        game = self.get_object()
        form = GameRatingForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data["rating"]
            GameRating.objects.update_or_create(
                user=request.user,
                game=game,
                defaults={"rating": rating},
            )
            return redirect("detail-top-games", slug=game.slug)
        else:
            return HttpResponseBadRequest("Invalid form data")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = self.get_object()
        ratings = game.ratings.aggregate(Avg("ratings__rating"))
        context["average_rating"] = ratings["ratings__rating__avg"]

        context["total_ratings"] = game.ratings.count()

        if self.request.user.is_authenticated:
            current_rating = GameRating.objects.filter(user=self.request.user, game=game).values_list("rating",
                                                                                                      flat=True).first()
        else:
            current_rating = None

        context["current_rating"] = current_rating
        context["form"] = GameRatingForm()
        return context


@login_required
def profile_view(request):
    user = request.user
    ratings = GameRating.objects.filter(user=user)
    future_releases = FutureReleases.objects.filter(voters=user)
    return render(request, "games_hub/profile.html", {"user": user, "ratings": ratings,
                                                      "future_releases": future_releases})
