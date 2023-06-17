from django.urls import path
from . import views


urlpatterns = [
    path("", views.MainPageView.as_view(), name="starting-page"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("signup", views.signup, name="signup"),
    path("future-releases", views.FutureReleasesPageView.as_view(), name="future-releases"),
    path("future-releases/<slug:slug>", views.DetailFutureReleasesPageView.as_view(), name="detail-future-releases"),
    path("future-releases/<slug:slug>/vote", views.vote_for_game, name="vote_for_game"),
    path("price-comparison", views.price_comparison, name="price-comparison-page"),
    path("price-comparison/results", views.price_comparison_results, name="results"),
    path("top-games", views.TopGamesPageView.as_view(), name="top-games"),
    path("top_games/<slug:slug>", views.DetailTopGamesPageView.as_view(), name="detail-top-games"),
    path("news/", views.MainPageView.as_view(), name="news-list"),
    path("profile/", views.profile_view, name="profile"),
    path("news/<slug:slug>", views.DetailNewsView.as_view(), name="detail-news-page"),
]
