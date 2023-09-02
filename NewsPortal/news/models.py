from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

class Author(models.Model):
    user_rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    # def update_rating(self):
    #     post_rating = Post.objects.filter(author=self).aggregate(Sum('post_rating')).get('post_rating__sum') * 3
    #     com_rating = self.coment.com_rating
    #     user_rating = self.user_rating
    # #     summ = int(post_rating + com_rating + user_rating)
    # #     return summ

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories')

    def __str__(self):
        return self.name

class Post(models.Model):
    NEWS = 'NW'
    ARTICLE = 'AR'
    Vibor = (
        (ARTICLE, "Статья"),
        (NEWS, "Новость"),
    )
    name_post = models.CharField(max_length=255)
    body_post = models.TextField()
    post_rating = models.IntegerField(default=0)
    time_post = models.DateTimeField(auto_now_add=True)
    vibor = models.CharField(max_length=2, choices=Vibor, default=ARTICLE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    def __str__(self):
        return f'{self.name_post}: {self.body_post[:40]}'

    # def like(self):
    #     return self.post_rating + 1
    #
    # def dislike(self):
    #     return self.post_rating - 1

    def preview(self):
        body_post = self.body_post
        body = body_post.split()
        return f"{body[:124]}..."

    # def get_absolute_url(self):
    #     return reverse('post_detail', args=[str(self.id)])

    def get_absolute_url(self):
        return f'/post/{self.id}'

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)

class Comment(models.Model):
    time_com = models.DateTimeField(auto_now_add=True)
    body_com = models.TextField()
    com_rating = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_com = models.ForeignKey(User, on_delete=models.CASCADE)
    #
    # def like(self):
    #     return self.com_rating + 1
    #
    # def dislike(self):
    #     return self.com_rating - 1


class CommonSignupForm(SignupForm):

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user

class Entrance(models.Model):
    enter = models.TextField()
