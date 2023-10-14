from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

SHOW_SYMBOLS = 30


class Group(models.Model):
    """Модель тематической группы постов."""

    title = models.CharField('Заголовок', max_length=200)
    slug = models.SlugField('Слаг', unique=True)
    description = models.TextField('Описание')

    class Meta:
        verbose_name = 'группа'
        verbose_name_plural = 'группы'
        ordering = ['id']

    def __str__(self):
        return self.title[:SHOW_SYMBOLS]


class Post(models.Model):
    """Модель публикации."""

    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='автор'
    )
    image = models.ImageField(
        upload_to='posts/',
        null=True,
        blank=True,
        verbose_name='изображение'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        verbose_name='группа',
        blank=True,
        null=True
    )

    class Meta:
        default_related_name = 'posts'
        verbose_name = 'публикация'
        verbose_name_plural = 'публикации'
        ordering = ['pub_date']

    def __str__(self):
        return self.text[:SHOW_SYMBOLS]


class Comment(models.Model):
    """Модель комментария."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='{author} прокомментировал:'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='публикация'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Отредактирован')

    class Meta:
        default_related_name = 'comments'
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created']

    def __str__(self):
        return (f'{self.author} прокомментировал '
                f'публикацию {self.post}: {self.text[:SHOW_SYMBOLS]}')


class Follow(models.Model):
    """Модель подписки."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь'
    )

    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follows',
        verbose_name='подписка на автора'
    )

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'], name='unique_follow'
            ),
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_prevent_self_follow',
                check=~models.Q(user=models.F('following')),
            ),
        ]

    def __str__(self):
        return (
            f'{self.user.username}'
            f'подписан на {self.following.username}'
        )
