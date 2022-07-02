from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.csrf import csrf_exempt 
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from app.models import IPTable
import re,uuid,time,threading,os,playsound
from django.conf import settings 


# Create your views here.
 

def loginRouter(request):  
    context = {"title": "Login"}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password) 
        if user is not None:
            login(request, user) 
            return redirect('dashboard')
        else: 
            return redirect('loginRouter')
 
    return render(request, 'app/login.html',context ) 


def logoutRouter(request):    
    logout(request)
    return redirect('loginRouter')




def getClientIP(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@login_required(login_url="/login/")
def dashboard(request):    
    context = {"title":"Dashboard"}
    print(getClientIP(request)) 
    # available_ips = IPTable.objects.all().order_by('allowed')
    available_ips = IPTable.objects.all().filter(waiting=False).order_by('allowed')
    
    context['available_ips'] = available_ips
    return render(request, 'app/dashboard.html',context ) 



@login_required(login_url="/login/")
@csrf_exempt
def changeAccessStatus(request):    
    val = str(request.POST['val']).lower()
    allowed = 'allow' in val  
    id = int(request.POST['id']) 
    required_ip = IPTable.objects.get(id=id)
    if allowed:
        required_ip.allowed = True
    else:
        required_ip.allowed = False 
    required_ip.waiting = False
    
    # print("Saving IP = ", required_ip.__dict__)
    
    required_ip.save() 
    return JsonResponse({})
 
 
 
 
 
 
 
@csrf_exempt
def getUUID(request):  
    unique_id = str(uuid.uuid4()) 
    ip = request.GET.get('ip')
    if not ip: 
        return JsonResponse({"response":"IP not attached"})
    validity = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",ip)
    if not validity: 
        return JsonResponse({"response":"Invalid IP address"})
    required_record = IPTable.objects.filter(ip=ip) 
    if required_record.exists():
        required_record = required_record.first()
        if required_record.allowed:
            return JsonResponse({"response": unique_id})
        else:
            if  required_record.waiting is False:
                return JsonResponse({"response": "Access Denied"})
    else:
        required_record = IPTable(ip=ip,waiting=True)
        required_record.save() 
    counter = 0
    while required_record.waiting:
        if counter>12:
            required_record.waiting = True
            required_record.save()
            return JsonResponse({"response": "Try Again"})
        time.sleep(3) 
        required_record = IPTable.objects.get(ip=ip)
        counter+=3 
    if required_record.allowed:
        return JsonResponse({"response": unique_id})
    else:
        if  required_record.waiting is False:
            return JsonResponse({"response": "Access Denied"})
    


 
 
def playNotificationAudio():
    audio_file_path = os.path.join(settings.MEDIA_ROOT,"beep_audio.mp3")
    print("playNotificationAudio")
    playsound.playsound( audio_file_path)

 
 
@csrf_exempt
def getWaitingList(request): 
    res = {}
    listed_ids = [int(x) for x in eval(request.GET['ids'])] 
    waiting_records = IPTable.objects.exclude(id__in=listed_ids) 
    if waiting_records:
        waiting_records = waiting_records.filter(waiting=True)
    
    res['waiting_records'] = [{"ip":x.ip,"id":x.id} for x in waiting_records] 
    if waiting_records: 
        audio_thread = threading.Thread(target=playNotificationAudio)
        audio_thread.start()
         
    return JsonResponse( res)