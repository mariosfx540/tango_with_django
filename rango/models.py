from django.db import models
from django.forms import ModelForm
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length=128, unique=True)
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	slug = models.SlugField()
	
	def save(self, *args, **kwargs):
		# Uncomment if you don't want the slug to change every time the name changes
		#if self.id is None:
			#self.slug = slugify(self.name)
		self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)
				

	def __unicode__(self): #For Python 2, use _str_ on Python 3
		return self.name
	
	
class Page(models.Model):
	category = models.ForeignKey(Category)
	title = models.CharField(max_length=128)
	url = models.URLField()
	views = models.IntegerField(default=0)
	
	def __unicode__(self):
		return self.title
	
class Ox(models.Model):
	horn_length = models.IntegerField()
	
	class Meta:
		ordering = ["horn_length"]
		verbose_name_plural = "oxen"

		
class PageForm(ModelForm):
	
	def clean(self):
		cleaned_data = self.cleaned_data
		url = cleaned_data.get('url')
		
		if url and not url.startwith('http://'):
			url = 'http://' + url
			cleaned_data['url'] = url
			
		return cleaned_data
	
class UserProfile(models.Model):
	user = models.OneToOneField(User)
	
	website = models.URLField(blank=True)
	picture = models.ImageField(upload_to='profile_images', blank=True)
	
	def __unicode__(self):
		return self.user.username