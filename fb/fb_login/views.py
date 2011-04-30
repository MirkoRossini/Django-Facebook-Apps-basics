# Create your views here.
import base64
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
import facebook
from md5 import md5
from models import *
from django.conf import settings

FACEBOOK_APP_ID = settings.FACEBOOK_APP_ID 
FACEBOOK_APP_SECRET = settings.FACEBOOK_APP_SECRET 
FACEBOOK_APP_NAME = settings.FACEBOOK_APP_NAME

import random 

### CHECK SIGNED REQUEST
import hmac
import hashlib


@csrf_exempt  #or post requests will be blocked
def canvas(request):
  
  try: #This assumes user just authorized the application
    sr = request.POST['signed_request']
  except KeyError:
    return HttpResponse("<script> top.location.href='%s'</script>"\
                            % 'http://apps.facebook.com/%s/' % FACEBOOK_APP_NAME)
  data = parse_signed_request(sr,FACEBOOK_APP_SECRET)
  
  
  user_id = data.get('user_id',False)
  oauth_token = data.get('oauth_token',False)
  
  try:
    u = FacebookUser.objects.get(id = user_id)
    user = u.user
  except FacebookUser.DoesNotExist:
    u = None 
  if not user_id or not oauth_token:
    #Need authorization for more data
    redirect_url = "https://www.facebook.com/dialog/oauth?client_id=%s&redirect_uri=%s&type=user_agent"\
                             % (FACEBOOK_APP_ID,'http://localhost:8000/canvas/')
                             #IMPORTANT! Change  url above accordingly 
    return HttpResponse("<script> top.location.href='%s'</script>" % redirect_url)
  f = facebook.GraphAPI(oauth_token)
  user_data = f.get_object(user_id)
  if u is None:
    username = user_data.get('username',user_id)
    password = md5(user_data.get('username','')+str(random.random())).hexdigest()
    user = User.objects.create_user(username = username,
                                email = '',
                                password = password,
                                )
    user.first_name = user_data.get('first_name','')
    user.last_name = user_data.get('last_name','')
    user.save()

    u = FacebookUser.objects.create(user = user,
				id = user_id) 
  return HttpResponse('<a href="/canvas/">/canvas/</a>')

def base64_url_decode(inp):
    padding_factor = (4 - len(inp) % 4) % 4
    inp += "="*padding_factor
    return base64.b64decode(unicode(inp).translate(dict(zip(map(ord, u'-_'), u'+/'))))

def parse_signed_request(signed_request, secret):

    l = signed_request.split('.', 2)
    encoded_sig = l[0]
    payload = l[1]

    sig = base64_url_decode(encoded_sig)
    data = simplejson.loads(base64_url_decode(payload))
    
    if data.get('algorithm').upper() != 'HMAC-SHA256':
        return None
    else:
        expected_sig = hmac.new(secret, msg=payload, digestmod=hashlib.sha256).digest()

    if sig != expected_sig:
        return None
    else:
        return data


