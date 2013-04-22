from django.db import models

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
	username = models.CharField(max_length=30)
	useremail = models.EmailField()
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


