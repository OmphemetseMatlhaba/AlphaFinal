from django.contrib import admin
from forum.models import Category, Comment, CommentDownvote, CommentUpvote, FarmerAchievement, SubCategory, Post, SubComment

# Register your models here.
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(SubComment)
admin.site.register(CommentUpvote)
admin.site.register(CommentDownvote)
admin.site.register(FarmerAchievement)