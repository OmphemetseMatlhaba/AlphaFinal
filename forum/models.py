import datetime
from django.db import models
from accounts.models import Achievements, BasicAccount
from ckeditor_uploader.fields import RichTextUploadingField 
from taggit.managers import TaggableManager
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image = models.ImageField(upload_to = 'forum/category_images', default='forum/category_images/default.jpg')

    class Meta:
        verbose_name = ('Category')
        verbose_name_plural = ('Categories')

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = ('SubCategory')
        verbose_name_plural = ('SubCategories')
    
    def __str__(self):
        return f"{self.category.name} => ({self.name})"
    
class Post(models.Model):
    farmer = models.ForeignKey(BasicAccount, on_delete=models.CASCADE, related_name='farmer')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = RichTextUploadingField()
    tags = TaggableManager()
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now)
    class Meta:
        verbose_name = ('Post')
        verbose_name_plural = ('Posts')
    
    def __str__(self):
        return self.title
    
class PostUpvote(models.Model):
    user = models.ForeignKey(BasicAccount, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

class PostDownvote(models.Model):
    user = models.ForeignKey(BasicAccount, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

class Comment(models.Model):
    farmer = models.ForeignKey(BasicAccount, on_delete=models.CASCADE, related_name='farmer_comment')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body 
    
    class Meta:
        verbose_name = ('Comment')
        verbose_name_plural = ('Comments')

class CommentUpvote(models.Model):
    user = models.ForeignKey(BasicAccount, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment')
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + ' liked ' + self.comment.body
    
class CommentDownvote(models.Model):
    user = models.ForeignKey(BasicAccount, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment')

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + ' disliked ' + self.comment.body
    
class SubComment(models.Model):
    farmer = models.ForeignKey(BasicAccount, on_delete=models.CASCADE, related_name='farmer_sub_comment')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    response = models.TextField()
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.response
    
    class Meta:
        verbose_name = ('Subcomment')
        verbose_name_plural = ('Subcomments')

class SubCommentUpvote(models.Model):
    user = models.ForeignKey(BasicAccount, on_delete=models.CASCADE)
    subcomment = models.ForeignKey(SubComment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'subcomment')

class SubCommentDownvote(models.Model):
    user = models.ForeignKey(BasicAccount, on_delete=models.CASCADE)
    subcomment = models.ForeignKey(SubComment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'subcomment')

class FarmerAchievement(models.Model):
    farmer = models.ForeignKey(BasicAccount, null=True, blank=True, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievements, on_delete=models.CASCADE)
    date_earned = models.DateTimeField(auto_now_add=True)