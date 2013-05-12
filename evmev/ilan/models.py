# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

# User Extension
from django.db.models.signals import post_save

class UserProfile(models.Model):  
	user = models.OneToOneField(User) 
	image = models.CharField(max_length=100,default='/static/defaultProfile.png')
	latt = models.FloatField(default=0)
	lng = models.FloatField(default=0)
	bilgi = models.CharField(max_length=255,default='Kendi hakkimda birsey yazmadim.')
    #other fields here

	def __str__(self):
		return "%s's profile" % self.user
	def set_coordinates(self,lat,lng):
		self.latt=lat
		self.lng=lng
		self.save()

def create_user_profile(sender, instance, created, **kwargs):  
    if created:
		profile, created = UserProfile.objects.get_or_create(user=instance)
		profile.first_name = instance.first_name
		profile.save()

post_save.connect(create_user_profile, sender=User) 


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
	


