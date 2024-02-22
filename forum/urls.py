from forum import views
from django.urls import path

urlpatterns = [
    path('', views.forum, name='forum'),
    path('sub_picker/<int:category_id>/', views.sub_picker, name='sub_picker'),
    path('sub_picker/<int:category_id>/<int:subcategory_id>/', views.sub_picker, name='sub_picker_with_subcategory'),
    path('create_post/', views.create_post, name='create_post'),
    path('create_post/get_subcategories/<int:category_id>/', views.get_subcategories, name='get_subcategories'),
    path('view_post/<int:post_id>', views.view_post, name='view_post'),
    path('upvote_post/<int:post_id>', views.upvote_post, name='upvote_post'),
    path('downvote_post/<int:post_id>', views.downvote_post, name='downvote_post'),
    path('comment_modal/<int:post_id>', views.comment_modal, name='comment_modal'),
    path('subcomment_modal/<int:comment_id>', views.subcomment_modal, name='subcomment_modal'),
    path('upvote_comment/<int:comment_id>', views.upvote_comment, name='upvote_comment'),
    path('downvote_comment/<int:comment_id>', views.downvote_comment, name='downvote_comment'),
    path('delete_post/<int:post_id>', views.delete_post, name='delete_post'),
    path('delete_comment/<int:comment_id>', views.delete_comment, name='delete_comment'),
    path('delete_sub_comment/<int:subcomment_id>', views.delete_sub_comment, name='delete_sub_comment'),
    path('edit_post/<int:post_id>', views.edit_post, name='edit_post'),
    path('posts_by_tag/<str:tag>/', views.posts_by_tag, name='posts_by_tag'),
    path('posts_by_date/<str:date>/', views.posts_by_date, name='posts_by_date'),
    path('posts_by_user/<int:user_id>/', views.posts_by_user, name='posts_by_user'),
    path('visit_user/<int:user_id>', views.visit_user, name='visit_user'),
    path('comment_achievement/<int:user_id>', views.posts_acheivement, name='longevity_achievement'),

]