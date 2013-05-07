from django.db import models
from django.contrib.auth.models import User

# User Extension
from django import template

register = template.Library()

@register.simple_tag
def get_username(user_id):
	print user_id
	try:
		return User.objects.get(id=user_id).username
	except User.DoesNotExist:
		return 'Unknown'

# Create your models here.
class ilan(models.Model):
	baslik = models.CharField(max_length=30,default='Bos')
	bolge = models.CharField(max_length=30)
	tarih = models.DateTimeField()
	fiyat = models.IntegerField()
	alan = models.IntegerField()
	imgname = models.CharField(max_length=40,default='default.jpg')
	imgname1 = models.CharField(max_length=40,default='')
	imgname2 = models.CharField(max_length=40,default='')
	imgname3 = models.CharField(max_length=40,default='')
#Coordinates
	latt = models.FloatField()
	lng = models.FloatField()
#User - Email
	user = models.ForeignKey(User)

	aciklama = models.CharField(max_length=200, default='...')
#Boolean
	bahce = models.BooleanField(default=False)
	internet = models.BooleanField(default=False)
	yatak = models.BooleanField(default=False)
	hayvan = models.BooleanField(default=False)
	balkon = models.BooleanField(default=False)
	teras = models.BooleanField(default=False)
	camasirmakinasi = models.BooleanField(default=False)
	bulasikmakinasi = models.BooleanField(default=False)

	

	def __unicode__(self):
		return self.baslik
		
class mesaj(models.Model):
	ilanid = models.IntegerField()
	msg = models.CharField(max_length=200, default='...')
	msgFrom = models.ForeignKey(User,related_name='mesaj_From')
	msgTo = models.ForeignKey(User,related_name='mesaj_To')
	msgSubject = models.CharField(max_length=50)
	


