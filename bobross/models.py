from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

# Create your models here.


class Paints(models.Model):
    color = models.CharField(max_length=100)
    amazon_link = models.CharField(max_length=100)
    amazon_html = models.CharField(max_length=600)

    class Meta:
        ordering = ('color',)

    def __str__(self):              # __unicode__ on Python 2
        return self.color


class Episode(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    wordcloud = models.ImageField(upload_to='bobross/media/wordclouds/',
                                  default='bobross/media/default_cloud.png')
    transcript = models.TextField()
    transcript_file = models.FileField(upload_to='bobross/media/transcripts')
    thumbnail = models.ImageField(upload_to='bobross/media/epi_thumbs',
                                  default='bobross/media/default.png')
    paints = models.ManyToManyField(Paints)
    yt_link = models.CharField(max_length=100, blank=True, default='')
    yt_id = models.CharField(max_length=100, blank=True, default='')
    painting = models.ImageField(upload_to='bobross/media/finished_paintings',
                                 default='bobross/media/default.png')
    season = models.IntegerField()
    episode_number = models.IntegerField()

    def __str__(self):              # __unicode__ on Python 2
        return self.title

    class Meta:
        ordering = ('season', 'episode_number')


class UserArt(models.Model):
    painting = models.ImageField(upload_to='user_paintings',
                                 default='bobross/media/default.png')
    owner = models.ForeignKey('auth.User', related_name='paintings')
    episode = models.ForeignKey(Episode, related_name='epi_paintings', default=1)

    def save(self, *args, **kwargs):
        """
        """
        super(UserArt, self).save(*args, **kwargs)


class UserArtForm(ModelForm):
    class Meta:
        model = UserArt
        fields = ['painting']









