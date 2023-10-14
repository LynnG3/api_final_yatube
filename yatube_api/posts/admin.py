from django.contrib import admin

from .models import Comment, Follow, Group, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Публикации отображены в админ-панели.
    Можно найти по тексту. Фильтр по дате добавления.
    """

    list_display = ('id', 'text', 'pub_date', 'author',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Группы отображены в админ-панели.
    Можно найти по заголовку или слагу. Можно сменить слаг.
    """

    list_display = ('title', 'description', 'slug',)
    list_editable = ('slug',)
    search_fields = (
        'title',
        'slug',
    )
    list_display_links = ('title',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Комментарии отображены в админ-панели.
    Можно найти по тексту или посту"""

    list_display = ('post', 'text',)
    search_fields = (
        "post",
        "text",
    )
    list_display_links = ('post',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Подписки отображены в админ-панели.
    Можно найти по автору или подписчику"""

    list_display = ('user', 'following',)
    search_fields = (
        'user',
        'following',
    )
    list_display_links = ('user', 'following')
