
from django.db import models

from django.db import models
from ckeditor.fields import RichTextField

class FAQCard(models.Model):
    tag = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='faq_images/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    details = RichTextField(max_length=4000,null=True, blank=True) 
    def __str__(self):
        return self.title
