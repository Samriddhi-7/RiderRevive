from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

# Create your models here.

class Post(models.Model):
    company = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    details = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)
    # pic=models.ImageField( upload_to='profile_pics')
    featured_images = models.ImageField(null=True, blank=True, default="default.jpg", upload_to='profile_pics')


    def __str__(self):
        return self.company

    def save(self):
        super().save()

        img = Image.open(self.featured_images.path)

        if img.height > 300 or img.width >300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.featured_images.path)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs= {'pk':self.pk})
