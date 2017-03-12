from django.conf import settings
from django.db import models


__all__ = (
    'Post',
    'PostLike',
)


class PostManager(models.Model):
    def visible(self):
        return super().get_queryset().filter(is_visible=True)


class PostUserVisibleManager(models.Model):
    def get_queryset(self):
        return super().get_queryset().filter(is_visible=True)


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    photo = models.ImageField(upload_to='post', blank=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='PostLike',
        related_name='Like_post_set',
    )
    created_date = models.DateTimeField(auto_now_add=True)
    is_visible = models.BooleanField(default=True)

    object = PostManager()

    visible = PostUserVisibleManager()

    def __str__(self):
        return 'Post[{}]'.format(self.id)

    class Meta:
        ordering = ('-id',)

    def toggle_like(self, user):
        pl_list = self.postlike_set.filter(user=user)
        # 현재 인자로 전달된 user가 좋아요 한적이 있는지 검사
        # if self.like_users.filter(id=user.id).exist():
        # if pl_list.exists():
        #     # 만약에 이미 좋아요를 했을 경우 해당 내역을 삭제
        #     # PostLike.objects.filter(post=self, user=user).delete()
        #     pl_list.delete()
        # # 아직 내역이 없을 경우 생성해준다.
        # else:
        #     PostLike.objects.create(post=self, user=user)
        # pl_list.delete if pl_list.exists() else PostLike.objects.create(post=self, user=user)
        return self.postlike_set.create(user=user) if not pl_list.exists() else pl_list.delete()

    def add_comment(self, user, content):
        return self.comment_set.create(
            author=user,
            content=content,
        )

    @property
    def like_count(self):
        return self.like_users.count()

    @property
    def comment_count(self):
        return self.comment_set.count()


class PostLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('user', 'post')
        )

    def __str__(self):
        return 'Post[{}]\'s Like[{}], User[{}]'.format(
            self.post_id,
            self.id,
            self.user_id
        )
