from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db import models


class News(models.Model):
    name = models.CharField(max_length=24)
    date = models.DateField(auto_now=True)
    excerpt = models.CharField(max_length=44)
    description = models.TextField()
    slug = models.SlugField(unique=True, db_index=True)
    preview_image = models.ImageField(upload_to="news", null=True)
    detail_image = models.ImageField(upload_to="news", null=True)

    def __str__(self):
        return f"{self.name} ({self.date})"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} ({self.created_date})"


class FutureReleases(models.Model):
    name = models.CharField(max_length=100)
    developer = models.CharField(max_length=100)
    release_date = models.DateField(blank=True, null=True)
    publisher = models.CharField(max_length=100, null=True)
    description_part1 = models.TextField()
    description_part2 = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="future_releases")
    trailer = models.CharField(max_length=100, null=True)
    slug = models.SlugField(unique=True, db_index=True)
    voters = models.ManyToManyField(User, blank=True, related_name="voted_games")

    def __str__(self):
        return f"{self.name} ({self.release_date})"


class TopGames(models.Model):
    name = models.CharField(max_length=100)
    developer = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100, null=True)
    release_date = models.DateField()
    description_part1 = models.TextField()
    description_part2 = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="top_games")
    trailer = models.CharField(max_length=100, null=True)
    slug = models.SlugField(unique=True, db_index=True)
    ratings = models.ManyToManyField(User, through="GameRating")

    def __str__(self):
        return self.name


class GameRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings")
    game = models.ForeignKey(TopGames, on_delete=models.CASCADE, related_name="game_ratings")
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    slug = models.SlugField(db_index=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.game.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} ({self.game}: {self.rating})"
