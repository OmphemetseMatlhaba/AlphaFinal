from django import forms
from forum.models import Comment, Post
from ckeditor.widgets import CKEditorWidget
from taggit.utils import require_instance_manager
from taggit.forms import TagField
from taggit.models import Tag


def clean_and_normalize_tags(tags):
    cleaned_tags = []
    for tag in tags:
        pascal_case_tag = tag.title().replace(" ", "")
        cleaned_tags.append(pascal_case_tag)
    return(cleaned_tags)

class CreatePostForm(forms.ModelForm):
    tags = forms.CharField(required=False, help_text="Separate tags using a comma (,)")

    def clean_tags(self):
        raw_tags = self.cleaned_data.get('tags', '')
        tag_list = [tag.strip() for tag in raw_tags.split(',') if tag.strip()]
        cleaned_tags = clean_and_normalize_tags(tag_list)
        return cleaned_tags

    class Meta:
        model = Post
        fields = ('category', 'sub_category', 'title', 'body', 'tags')
        
    def __init__(self, *args, **kwargs):
        super(CreatePostForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
    
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body',)

    def __init__(self, *args, **kwargs):
        super(EditPostForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'