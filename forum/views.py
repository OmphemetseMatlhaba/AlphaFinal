import datetime
import os
from time import strftime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from dateutil.relativedelta import relativedelta
import joblib
from accounts.models import AdditionalInfo, BasicAccount
from forum.forms import CommentForm, CreatePostForm, EditPostForm
from forum.models import Category, Comment, CommentDownvote, CommentUpvote, FarmerAchievement, Post, PostDownvote, PostUpvote, SubCategory, SubComment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
import bleach
from django.db.models import DateField
from django.db.models.functions import Cast
from django.db.models import Count


# Create your views here.
model = os.path.join(os.path.dirname(__file__), 'model', 'model2ZA.pkl')
cb_model = joblib.load(model)
count_vectorizer = os.path.join(os.path.dirname(__file__), 'model', 'count_vectorizer.pkl')
cv = joblib.load(count_vectorizer)

def forum(request):
    categories = Category.objects.all().prefetch_related('subcategory_set')
    
    context = {
        'categories': categories
    }

    if request.user.is_authenticated:
        context['profile_picture'] = request.user.profile.profile_picture
        longevity_achievement(request, user_id=request.user.id)
    return render(request, 'forum/main.html', context)

def sub_picker(request, category_id, subcategory_id=None):
    categories = Category.objects.all().prefetch_related('subcategory_set')
    category = Category.objects.get(id=category_id)
    subcategories = category.subcategory_set.all()

    if subcategory_id:
        selected_subcategory = SubCategory.objects.get(id=subcategory_id)
        posts = Post.objects.filter(sub_category=selected_subcategory)
    else:
        selected_subcategory = None
        posts = Post.objects.filter(category=category)

    context = {
        'categories': categories,
        'category': category,
        'subcategories': subcategories,
        'posts': posts,
    }
    if request.user.is_authenticated:
        context['profile_picture'] = request.user.profile.profile_picture

    return render(request, 'forum/sub_picker.html', context)

@login_required(login_url='login')
def create_post(request):
    categories = Category.objects.all().prefetch_related('subcategory_set')
    farmer = request.user

    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            input = form.cleaned_data['body']
            processed_input = cv.transform([input]).toarray()
            response = cb_model.predict(processed_input)
            if response == 'No Hate and Offensive Speech':
                post_form = form.save(commit = False)
                post_form.farmer = farmer
                post_form.created_at = datetime.datetime.now()
                post_form.upvotes = 0
                post_form.save()
                form.save_m2m()
                posts_acheivement(request, farmer.id)
                messages.success(request, "Post created successfully")
                return redirect('forum')    
            else:
                messages.error(request, "Your post has been flagged as innapropriate or offensive")
                return redirect('create_post')
        else:
            messages.error(request, "Something went wrong. try again later")
            return redirect('create_post')
    else:
        form = CreatePostForm()

    context = {
        'categories': categories,
        'form': form,
    }
    if request.user.is_authenticated:
        context['profile_picture'] = request.user.profile.profile_picture
    return render(request, 'forum/create_post.html', context)


def get_subcategories(request, category_id):
    subcategories = SubCategory.objects.filter(category_id=category_id)
    data = [{
            'id': subcategory.id, 
            'name': subcategory.name
            } 
        for subcategory in subcategories
        ]
    return JsonResponse(data, safe=False)

ALLOWED_TAGS = [
    'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'strong', 'ul',
    'p', 'br', 'span', 'div', 'hr', 'img', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'
]

ALLOWED_ATTRIBUTES = {
    '*': ['class', 'style'],
    'a': ['href', 'title', 'target'],
    'abbr': ['title'],
    'acronym': ['title'],
    'img': ['src', 'alt'],
}

@login_required(login_url='login')
def view_post(request, post_id):
    post = Post.objects.get(id=post_id)
    sanitized_body = bleach.clean(post.body, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
    categories = Category.objects.all().prefetch_related('subcategory_set')
    user = request.user
    comments = Comment.objects.filter(post=post_id)
    
    sanitized_comment_body = None
    
    for comment in comments:
        sanitized_comment_body = bleach.clean(comment.body, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)

    sub_count = 0
    user_upvoted_comment = None
    user_downvoted_comment = None
    

    sub_comments = {}   
    for comment in comments:
        replies = SubComment.objects.filter(comment = comment)
        sub_comments[comment.id] = replies
        sub_count = len(sub_comments[comment.id])
       
    upvoted_comments = CommentUpvote.objects.filter(user=request.user).values_list('comment_id', flat=True)
    downvoted_comments = CommentDownvote.objects.filter(user=request.user).values_list('comment_id', flat=True)

    
    user_upvoted_post = PostUpvote.objects.filter(user=user, post=post).exists()
    user_downvoted_post = PostDownvote.objects.filter(user=user, post=post).exists()
    
    existing_comment = Comment.objects.filter(post=post, farmer=request.user).first()
    if request.method == 'POST':
        com_form = CommentForm(request.POST, instance=existing_comment)
        comment_form = None  # Define comment_form before the conditional block
        if com_form.is_valid():
            input = com_form.cleaned_data['body']
            processed_input = cv.transform([input]).toarray()
            response = cb_model.predict(processed_input)
            if response == 'No Hate and Offensive Speech':
                comment_form = com_form.save(commit=False)
                comment_form.farmer = request.user
                comment_form.post = post
                comment_form.save()
                comment_owner = comment_form.farmer.id if comment_form else None
                comment_achievement(request, comment_owner)
                messages.success(request, 'comment saved')
            else:
                messages.error(request, 'Your Comment has been flagged as inappropriate')
            
            return redirect('view_post', post_id=post.id)

    else:
        com_form = CommentForm(instance = existing_comment)


    total_comments = comments.count() + sub_count    

    context = {
        'categories': categories,
        'post': post,
        'sanitized_body': sanitized_body,
        'comments': comments,
        'sanitized_comment_body': sanitized_comment_body,
        'sub_comments': sub_comments,
        'total_comments': total_comments,
        'user_upvoted_post': user_upvoted_post,
        'user_downvoted_post': user_downvoted_post,
        'upvoted_comments': upvoted_comments,
        'downvoted_comments': downvoted_comments,
        'com_form': com_form,
        'existing_comment': existing_comment
    }

    if request.user.is_authenticated:
        context['profile_picture'] = request.user.profile.profile_picture
    return render(request, 'forum/post_details.html', context)

def upvote_post(request, post_id):
    post = Post.objects.get(id = post_id)
    user = request.user

    upvote_query = PostUpvote.objects.filter(user=user, post=post)
    downvote_query = PostDownvote.objects.filter(user=user, post=post)

    if upvote_query.exists():
        upvote_query.delete()
        post.upvotes -= 1
    else:
        PostUpvote.objects.create(user=user, post=post)
        post.upvotes += 1
        if downvote_query.exists():
            downvote_query.delete()
            post.downvotes -= 1
            
    
    post.save()
    post_owner = post.farmer.id
    like_achievement(request, post_owner)
    return redirect('view_post', post_id=post.id)

def downvote_post(request, post_id):
    post = Post.objects.get(id = post_id)
    user = request.user

    downvote_query = PostDownvote.objects.filter(user=user, post=post)
    upvote_query = PostUpvote.objects.filter(user=user, post=post)

    if downvote_query.exists():
        downvote_query.delete()
        post.downvotes -= 1
    else:
        PostDownvote.objects.create(user=user, post=post)
        post.downvotes += 1 
        if upvote_query.exists():
            upvote_query.delete()
            post.upvotes -= 1 
    
    post.save()
    return redirect('view_post', post_id=post.id)

def comment_modal(request, post_id):
    post = Post.objects.get(id=post_id)
    body = request.POST.get('post_body')

    existing_comment = Comment.objects.filter(post=post, farmer=request.user.id).first()

    if existing_comment:
        existing_comment.body = body
        processed_input = cv.transform([body]).toarray()
        response = cb_model.predict(processed_input)
        if response == 'No Hate and Offensive Speech':
            existing_comment.farmer = request.user.id
            existing_comment.save()
            messages.success(request, 'Comment updated successfully')
        else:
            messages.error(request, 'Your comment has been flagged as innapropriate and will be removed')
        return redirect('view_post', post_id=post.id)
    else:
        
        comment = Comment(
            body=body,
            post=post,
            farmer=request.user.id,
        )
        comment.save()
        messages.success(request, 'Comment saved successfully')
        

    context = {
        'post': post,
        'existing_comment': existing_comment,
    }
    return render(request, 'forum/post_details.html', context)


def subcomment_modal(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    sub_comment_body = request.POST.get('sub_comment_body')

    if request.method == 'POST':
        input = sub_comment_body
        processed_input = cv.transform([input]).toarray()
        response = cb_model.predict(processed_input)
        if response == 'No Hate and Offensive Speech':
            subcomment = SubComment(
                farmer = request.user,
                comment = comment,
                response = sub_comment_body,
            )
            subcomment.save()
            sub_comment_owner = subcomment.farmer.id
            subcomment_achievements(request, sub_comment_owner)
            messages.success(request, 'Comment response saved successfully')
        else:
            messages.error(request, 'Your comment has been flagged as innapropriate or hateful')
        return redirect('view_post', post_id=comment.post.id)
    
    context = {
        'comment': comment,
    }
    return render(request, 'forum/post_details.html', context)

def upvote_comment(request, comment_id):
    url = request.META.get('HTTP_REFERER')
    comment = Comment.objects.get(id=comment_id)
    user = request.user

    upvote_query = CommentUpvote.objects.filter(user=user, comment=comment)
    downvote_query = CommentDownvote.objects.filter(user=user, comment=comment)

    if upvote_query.exists():
        upvote_query.delete()
        comment.upvotes -= 1

    else:
        CommentUpvote.objects.create(user=user, comment=comment)
        comment.upvotes += 1
        if downvote_query.exists():
            downvote_query.delete()
            comment.downvotes -= 1
    
    comment.save()
    return redirect(url)

def downvote_comment(request, comment_id):
    url = request.META.get('HTTP_REFERER')
    comment = Comment.objects.get(id=comment_id)
    user = request.user

    upvote_query = CommentUpvote.objects.filter(user=user, comment=comment)
    downvote_query = CommentDownvote.objects.filter(user=user, comment=comment)

    if downvote_query.exists():
        downvote_query.delete()
        comment.downvotes -= 1
    else:
        CommentDownvote.objects.create(user=user, comment=comment)
        comment.downvotes += 1
        if upvote_query.exists():
            upvote_query.delete()
            comment.upvotes -= 1
    
    comment.save()
    return redirect(url)

def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user == post.farmer:
        post.delete()
        messages.success(request, "Post deleted")
    else:
        messages.error(request, "You cannot delete a comment that's not yours!")
    return redirect('forum')

def delete_comment(request, comment_id):
    url = request.META.get('HTTP_REFERER')
    comment = Comment.objects.get(id = comment_id)
    if request.user == comment.farmer:
        comment.delete()
        messages.success(request, "Comment deleted")
    else:
        messages.error(request, "You cannot delete a comment that's not yours!")
    return redirect(url)

def delete_sub_comment(request, subcomment_id):
    url = request.META.get('HTTP_REFERER')
    subcomment = SubComment.objects.get(id = subcomment_id)
    if request.user == subcomment.farmer:
        subcomment.delete()
        messages.success(request, "Reply deleted")
    else:
        messages.error(request, "You cannot delete a response that's not yours!")
    return redirect(url)


def edit_post(request, post_id = None):
    post = Post.objects.get(id = post_id)
    categories = Category.objects.all().prefetch_related('subcategory_set')
    if request.method == 'POST':
        form = EditPostForm(request.POST, instance=post)
        if form.is_valid():
            edit_form = form.save(commit=False) 
            edit_form.updated_at = datetime.datetime.now()
            edit_form.save()
            messages.success(request, "Post updated successfully")
            return redirect('view_post', post_id=post.id)
    else:
        form = EditPostForm(instance=post)

    context = {
        'form': form,
        'categories': categories,

    }
    if request.user.is_authenticated:
        profile = AdditionalInfo.objects.get(user = request.user )
        context['profile_picture'] = profile.profile_picture
    return render(request, "forum/edit_post.html", context) 
    
def posts_by_tag(request, tag):    
    posts = Post.objects.filter(tags__name=tag).order_by('created_at')
    categories = Category.objects.all().prefetch_related('subcategory_set')
    context = {
        'posts': posts,
        'tag': tag,
        'categories': categories,
        }
    if request.user.is_authenticated:
        context['profile_picture'] = request.user.profile.profile_picture
    return render(request, 'forum/tag_posts.html', context)

def posts_by_date(request, date):
    posts = Post.objects.annotate(created_date=Cast('created_at', DateField())).filter(created_date=date).order_by('created_at')
    categories = Category.objects.all().prefetch_related('subcategory_set')
    context = {
        'posts': posts,
        'categories': categories,
        'date': date,
    }
    if request.user.is_authenticated:
        context['profile_picture'] = request.user.profile.profile_picture
    return render(request, 'forum/date_posts.html', context)

def posts_by_user(request, user_id):
    posts = Post.objects.filter(farmer=user_id).order_by('created_at')
    categories = Category.objects.all().prefetch_related('subcategory_set')
    
    context = {
        'posts': posts,
        'categories': categories,
    }
    if request.user.is_authenticated:
        context['profile_picture'] = request.user.profile.profile_picture
    return render(request, 'forum/user_posts.html', context)
    
def like_achievement(request, user_id):

    farmer = get_object_or_404(BasicAccount, id=user_id)
    like_count = farmer.get_total_upvotes()


    if like_count >= 10:
        FarmerAchievement.objects.get_or_create(farmer=farmer, achievement_id=19)
    if like_count >= 30:
        FarmerAchievement.objects.get_or_create(farmer=farmer, achievement_id=20)
    if like_count >= 50:
        FarmerAchievement.objects.get_or_create(farmer=farmer, achievement_id=21)
    if like_count <= 50:
        print("Not Yet")

def comment_achievement(request, user_id):
    farmer = get_object_or_404(BasicAccount, id=user_id)
    comment_count = farmer.get_total_comments()
    print(comment_count)

    if comment_count >= 5:
        FarmerAchievement.objects.get_or_create(farmer=farmer, achievement_id=10)
        print('level 1')
    if comment_count >= 15:
        FarmerAchievement.objects.get_or_create(farmer=farmer, achievement_id=11)
        print('level 2')
    if comment_count >= 30:
        FarmerAchievement.objects.get_or_create(farmer=farmer, achievement_id=12)
        print('level 3')
    else:
        print('Not yet')

def longevity_achievement(request, user_id):
    farmer = BasicAccount.objects.get(id=user_id)
    created_date_raw = farmer.date_joined
    created_date = created_date_raw.strftime('%Y-%m-%d')
    one_year_later = (created_date_raw + relativedelta(years=1)).strftime('%Y-%m-%d')
    two_years_later = (created_date_raw + relativedelta(years=2)).strftime('%Y-%m-%d')
    three_years_later = (created_date_raw + relativedelta(years=3)).strftime('%Y-%m-%d')
    four_years_later = (created_date_raw + relativedelta(years=4)).strftime('%Y-%m-%d')
    five_years_later = (created_date_raw + relativedelta(years=5)).strftime('%Y-%m-%d')
    today = datetime.date.today().strftime('%Y-%m-%d')
    
    if today >= one_year_later:
        FarmerAchievement.objects.get_or_create(farmer=farmer, achievement_id=5)
        print('level 1')
    if today >= two_years_later:
        FarmerAchievement.objects.get_or_create(farmer=farmer, achievement_id=6)
        print('level 2')
    if today >= three_years_later:
        FarmerAchievement.objects.get_or_create(farmer=farmer, achievement_id=7)
        print('level 3')
    if today >= four_years_later:
        FarmerAchievement.objects.get_or_create(farmer=farmer, achievement_id=8)
        print('level 4')
    if today >= five_years_later:
        FarmerAchievement.objects.get_or_create(farmer=farmer, achievement_id=4)
        FarmerAchievement.objects.get_or_create(farmer=farmer, achievement_id=9)
        print('level 6')
        print('level 5')
    if today <= one_year_later:
        print('keep using the system')

def posts_acheivement(request, user_id):
    farmer = BasicAccount.objects.get(id = user_id)
    number_of_posts = farmer.get_total_posts()
    
    if number_of_posts >= 5:
        FarmerAchievement.objects.get_or_create(farmer=farmer, achievement_id=1)
        print('level 1')
    if number_of_posts >= 10:
        FarmerAchievement.objects.get_or_create(farmer=farmer, achievement_id=2)
        print('level 2')
    if number_of_posts >= 20:
        FarmerAchievement.objects.get_or_create(farmer=farmer, achievement_id=3)
        print('level 3')

def subcomment_achievements(request, user_id):
    farmer = BasicAccount.objects.get(id = user_id)
    number_of_subcomments = farmer.get_total_subcomments()

    if number_of_subcomments >= 10:
        FarmerAchievement.objects.get_or_create(farmer=farmer, achievement_id=13)
        print('level 1')
    if number_of_subcomments >= 30:
        FarmerAchievement.objects.get_or_create(farmer=farmer, achievement_id=14)
        print('level 2')
    if number_of_subcomments >= 50:
        FarmerAchievement.objects.get_or_create(farmer=farmer, achievement_id=15)
        print('level 3')
    if number_of_subcomments < 10:
        print('keep commenting')

def visit_user(request, user_id):
    farmer = BasicAccount.objects.get(id = user_id)
    total_posts = farmer.get_total_posts()
    total_upvotes = farmer.get_total_upvotes()
    total_downvotes = farmer.get_total_downvotes()
    total_engagement = total_upvotes + total_downvotes
    farm_info = farmer.farm_info.get()

    if total_upvotes > 0 or total_downvotes > 0:
        alpha_rating_raw = (total_upvotes / total_engagement) * 100
        alpha_rating = round(alpha_rating_raw, 2)
    else:
        alpha_rating = 0
    

    latest_posts = Post.objects.filter(farmer=user_id).order_by('-created_at')[:3]
    badges = FarmerAchievement.objects.filter(farmer=user_id)

    context = {
        'farmer': farmer,
        'total_posts': total_posts,
        'total_upvotes': total_upvotes,
        'alpha_rating': alpha_rating,
        'total_downvotes': total_downvotes,
        'farm_info': farm_info,
        'latest_posts': latest_posts,
        'badges': badges,
    }
    if request.user.is_authenticated:
        context['profile_picture'] = request.user.profile.profile_picture
    return render(request, 'forum/user_profile.html', context)


