# import random
#
# from django.db import models, IntegrityError
#
#
#
#
# class MyUser(models.Model):
#     # username, last_name, first_name 등등 설정
#     username = models.CharField('유저네임', max_length=30, unique=True)
#     last_name = models.CharField('성', max_length=15)
#     first_name = models.CharField('이름', max_length=15)
#     nickname = models.CharField('닉네임', max_length=30)
#     email = models.EmailField('이메일', blank=True)
#     date_joined = models.DateField(auto_now_add=True)
#     last_modified = models.DateField(auto_now=True)
#     following = models.ManyToManyField(
#         'self',
#         blank=True,
#         related_name='follower_set',
#         # 다대다 관계에서 쌍방향이 아니고 한방향 관계가 되도록 설정
#         # following이면 일방적인 관계이므로 한방향이다.
#         symmetrical=False,
#     )
#
#     def __str__(self):
#         return self.username
#
#     def follow(self, user):
#         self.following.add(user)
#
#     def unfollow(self, user):
#         self.following.remove(user)
#
#     # 읽기 전용
#     @property
#     def followers(self):
#         return self.follower.set.all()
#
#     def change_nickname(self, new_nickname):
#         self.nickname = new_nickname
#         self.save()
#
#     @staticmethod
#     def create_dummy_user(num):
#         """
#         num 개수만큼 User1 ~ User<num>까지 임의의 유저를 생성한다
#         """
#         last_name_list = ['홈즈', '왓슨', '모리아티', '애들러']
#         first_name_list = ['셜록', '존', '짐', '아이린']
#         nickname_list = ['sherlock', 'John', 'Mori', 'Ad']
#         created_count = 0
#         for i in range(num):
#             try:
#                 MyUser.objects.create(
#                     username='User{}'.format(i + 1),
#                     last_name=random.choice(last_name_list),
#                     first_name=random.choice(first_name_list),
#                     nickname=random.choice(nickname_list),
#                 )
#                 created_count += 1
#             except IntegrityError as e:
#                 print(e)
#         return created_count
#
#     @staticmethod
#     def assign_global_variables():
#         # sys모듈은 파이썬 인터프리터 관련 내장모듈
#         import sys
#         # __main__  모듈을 module 변수에 할당
#         module = sys.modules['__main__']
#         # MyUser 객체 중 'User'로 시작하는 객체들만 조회하여 users 변수에 할당
#         users = MyUser.objects.filter(username__startswith='User')
#
#         # users를 순회하며
#         for index, user in enumerate(users):
#             # __main__모듈에 'u1, u2, u3 ...' 이름으로 각 MyUser 객체를 할당
#             setattr(module, 'u{}'.format(index + 1), user)