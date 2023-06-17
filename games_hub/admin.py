from .models import News, FutureReleases, TopGames, GameRating, Comment
from django.contrib import admin


class NewsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class FutureReleasesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class TopGamesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(News, NewsAdmin)
admin.site.register(FutureReleases, FutureReleasesAdmin)
admin.site.register(TopGames, TopGamesAdmin)
admin.site.register(GameRating)
admin.site.register(Comment)
