# Create your views here.
from django.template import RequestContext, Context, Template
from django.shortcuts import render_to_response, get_object_or_404,render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.utils import simplejson
from django.core.cache import cache
from django.core.mail import send_mail
from django.core import serializers
from django.db.models import Q
import uuid
import datetime
from evmev.ilan.models import ilan, mesaj, UserProfile
from evmev.ilan.forms import ContactForm
from django.contrib.auth.models import User


def home(request):
	#UserProfile.objects.get_or_create(user=request.user)
	print request.user
	if request.user != "AnonymousUser":# and request.user.get_profile().latt == 0:
		import pygeoip
		x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
		if x_forwarded_for:
			ip = x_forwarded_for.split(',')[-1].strip()
		else:
			ip = request.META.get('REMOTE_ADDR')
	####--localhost---##
		if ip == '127.0.0.1':
			ip = '145.97.237.229'
	####-------------------
		gi = pygeoip.GeoIP('/app/static/geoip/GeoLiteCity.dat')
		user_location = gi.record_by_addr(ip)
		print ip,user_location
		request.user.get_profile().set_coordinates(user_location['latitude'],user_location['longitude']) 	
	c = {}
	c.update(csrf(request))
	context = RequestContext(request, c)
	return render_to_response("home.html", context)

@login_required('')
def ekle(request):
	c = {}
	c.update(csrf(request))
	context = RequestContext(request, c)
	return render_to_response("ekle.html", context)

def ara(request):
	c = {}
	c.update(csrf(request))
	context = RequestContext(request, c)
	return render_to_response("ara.html", context)

def getir(request):
	response_data = ilan.objects.filter(latt__range=([request.POST['s'],request.POST['n']])).filter(lng__range=(request.POST['w'],request.POST['e']))
	return HttpResponse(serializers.serialize('json',response_data), mimetype="application/json")

def hakkinda(request):
	c = {}
	c.update(csrf(request))
	context = RequestContext(request, c)
	return render_to_response("hakkinda.html",context)

def set_geoip(request):
	gi = pygeoip.GeoIP('/app/static/geoip/GeoLiteCity.dat')
	user_location = gi.record_by_addr('64.233.161.99')
	request.user.get_profile().set_coordinates(user_location.lat_lon[0],user_location.lat_lon[1])
def set_user_image(request):
	print 'fonk'
	if request.method == 'POST':
		user = request.user.get_profile()
		print user.image
		user.image = request.POST['image']
		print user.image
		user.save()
		print user.image
	return HttpResponse("OK")
def set_user_coordinates(request):
	if request.method == 'POST':
		request.user.get_profile().set_coordinates(request.POST['lat'],request.POST['lng'])
	return HttpResponse("OK")
def iletisim(request):
	if request.method == 'POST':
		form = ContactForm(request.POST) 
		if form.is_valid():
			subject = form.cleaned_data['subject']
			message = form.cleaned_data['message']
			sender = form.cleaned_data['sender']
			recipients = ['alpdeniz@gmail.com',]   
			try:		
				send_mail(subject, message, sender, recipients)
			except:
				pass
			c = {}
			c.update(csrf(request))
			context = RequestContext(request, c)
			return render_to_response("gonderildi.html",context)
		return HttpResponseRedirect('/iletisim/') # Redirect after POST
	form = ContactForm() # An unbound form
	return render(request, 'iletisim.html', {'form': form })
	
@login_required('')
def profile(request,user_id = ""):
	print request.user.get_profile()
	c = {}
	c.update(csrf(request))
	c['user_id'] = user_id
	c['ilans'] = ilan.objects.filter(user=request.user)
	context = RequestContext(request, c)
	return render_to_response("profile.html", context)
@login_required('')
def mesajlar(request,kutu = ""):
	if request.method == 'POST':
		message = request.POST['mesaj']
		recipients=[ilan.objects.filter(pk = request.POST['ilanid'])[0].user.email]
		sender = request.user.email
		subject = 'Evmev - ilaniniz icin mesaj var'
		try:
			send_mail(subject, message, sender, recipients)
		except:
			pass
		msg = mesaj()
		msg.ilanid = request.POST['ilanid']
		msg.msg = message
		msg.msgTo = User.objects.get(pk=request.POST['msgTo'])
		msg.msgFrom = request.user
		msg.msgSubject = request.POST['ilanid']
		msg.save()
			
	msgList = mesaj.objects.filter(Q(msgFrom=request.user) | Q(msgTo=request.user))
	#msgList = mesaj.objects.all()
	a = mesaj.objects.filter(Q(msgFrom=request.user) | Q(msgTo=request.user))	
	#a = mesaj.objects.all()
	b = []
	couples = []
	#froms.append(request.user.id)
	for msg in msgList:	
		if msg.msgFrom.id != request.user.id and [msg.ilanid,msg.msgFrom.id] not in couples:			
			b.append(a.filter(ilanid = msg.ilanid).filter(Q(msgTo=msg.msgFrom) | Q(msgFrom=msg.msgFrom)))
			couples.append([msg.ilanid,msg.msgFrom.id])
		if msg.msgTo.id != request.user.id and [msg.ilanid,msg.msgTo.id] not in couples:			
			b.append(a.filter(ilanid = msg.ilanid).filter(Q(msgTo=msg.msgTo) | Q(msgFrom=msg.msgTo)))
			couples.append([msg.ilanid,msg.msgTo.id])	
	c = {}
	c.update(csrf(request))
	c["msgList"] = b
	context = RequestContext(request, c)
	return render_to_response("mesajlar.html",context)
	

@login_required('')
def kaydet(request):
	ad = ilan()
	ad.user = request.user
	ad.bolge = ''
	ad.aciklama = request.POST['aciklama']
	ad.fiyat = request.POST['price']
	ad.alan = request.POST['area']
	ad.imgname = request.POST.get('imgname0', 'default.jpg')
	ad.imgname1 = request.POST.get('imgname1', '')
	ad.imgname2 = request.POST.get('imgname2', '')
	ad.imgname3 = request.POST.get('imgname3', '')
	ad.latt = request.POST['lat']
	ad.lng = request.POST['lon']
	ad.tarih = datetime.datetime.now()
	
	ad.bahce = request.POST.get('bahce', False)
	ad.internet = request.POST.get('internet', False)
	ad.hayvan = request.POST.get('hayvan', False)
	ad.balkon = request.POST.get('balkon', False)
	ad.teras = request.POST.get('teras', False)
	ad.camasirmakinasi = request.POST.get('camasirmakinasi', False)
	ad.bulasikmakinasi = request.POST.get('bulasikmakinasi', False)
	ad.save()
	c = {}
	c.update(csrf(request))
	c['kayit'] = "<div style='background-color:#3a5;' class='well span8 offset2'>Ilaniniz basariyla kayit edildi. Ilani gormek icin <a href='/ilan/goster/" + str(ad.id) +"'>tiklayiniz</a></div>"
	context = RequestContext(request, c)
	return render_to_response("home.html",context)

def goster(request, ilan_id):
	ad = get_object_or_404(ilan, pk=ilan_id)
	return render(request, 'goster.html', {'ilan': ad })

def save_upload( uploaded, filename, raw_data ):
  
  '''
  raw_data: if True, uploaded is an HttpRequest object with the file being
            the raw post data
            if False, uploaded has been submitted via the basic form
            submission and is a regular Django UploadedFile in request.FILES
  '''
  try:
    from io import FileIO, BufferedWriter
    with BufferedWriter( FileIO( filename, "wb" ) ) as dest:
      # if the "advanced" upload, read directly from the HTTP request
      # with the Django 1.3 functionality
      if raw_data:
        foo = uploaded.read( 1024 )
        while foo:
          dest.write( foo )
          foo = uploaded.read( 1024 )
      # if not raw, it was a form upload so read in the normal Django chunks fashion
      else:
        for c in uploaded.chunks( ):
          dest.write( c )
      # got through saving the upload, report success
      return True
  except IOError:
    # could not open the file most likely
    pass
  return False
 
def upload( request ):
  if request.method == "POST":   
    if request.is_ajax( ):
      # the file is stored raw in the request
      upload = request
      is_raw = True
      # AJAX Upload will pass the filename in the querystring if it is the "advanced" ajax upload
      try:
        filename = request.GET[ 'qqfile' ]
		#filename = uuid.uuid4()
      except KeyError:
        return HttpResponseBadRequest( "AJAX request not valid" )
    # not an ajax upload, so it was the "basic" iframe version with submission via form
    else:
      is_raw = False
      if len( request.FILES ) == 1:
        # FILES is a dictionary in Django but Ajax Upload gives the uploaded file an
        # ID based on a random number, so it cannot be guessed here in the code.
        # Rather than editing Ajax Upload to pass the ID in the querystring,
        # observer that each upload is a separate request,
        # so FILES should only have one entry.
        # Thus, we can just grab the first (and only) value in the dict.
        upload = request.FILES.values( )[ 0 ]
      else:
        raise Http404( "Bad Upload" )
      filename = upload.name
     
    # save the file
    filename = str(uuid.uuid4()) + '.' +filename[-3:]
    path = 'static/img/'+ filename
    success = save_upload( upload, path, is_raw )
 
    # let Ajax Upload know whether we saved it or not
    import json
    ret_json = { 'success': filename, }
    return HttpResponse( json.dumps( ret_json ) )
