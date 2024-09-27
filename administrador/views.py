from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.http import HttpResponse

from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.decorators import otp_required

# Create your views here.
from . import correo
from . import utils

import bleach

class Login(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return render(request,"admin/index/login.html")
        return redirect('../../../../../../../admin/dashboard/')
    
    def post(self,request):
        if not request.user.is_authenticated:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            print(request.POST)
            if user is not None:
                login(request, user)
                if user.action_verify == False:
                    return redirect('../../../../../../../../../admin/dashboard/')
                else:
                    user.verify = False
                    user.save()
                    return redirect("../../../../../../../admin/verificar/")
            else:
                return render(request, 'admin/index/login.html', {'error': 'Invalid username or password'})
        return redirect('../../../../../../../admin/dashboard/')


def Logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("../../../../../../../../admin/")




class Panel(View):
    def get(self,request):
        if request.user.is_authenticated:
            if request.user.action_verify and request.user.verify == False:
                return redirect("../../../../../../../admin/verificar/")
            
            request.user.tocken = ""
            request.user.save()
            return render(request,"admin/panel/dashboard.html")
        return redirect("../../../../../../../../../../../admin/")



class backend_verificacion_email(View):
    def get(self, request, opc:int):
        if request.user.is_authenticated:
            if request.user.action_verify and request.user.verify == False:
                return redirect("../../../../../../../admin/verificar/")
            
            tocken = utils.get_tocken()
            request.user.tocken = tocken
            request.user.save()
            if opc == 1:
                Asunto = "Confirmacion para Habilitar 2FA"
                Mensaje = f'''
Hola {request.user.username},

Tu solicitud para habilitar la autenticación de dos factores (2FA) ha sido recibida. 
Para completar el proceso, por favor utiliza el siguiente código de confirmación:

Código de Confirmación: {tocken}

Si no has solicitado habilitar el 2FA, por favor ignora este mensaje o contacta con nuestro soporte.

Gracias,
El equipo de webditech

    '''
                correo.enviar_correo(email=request.user.email,Asunto=Asunto,s=Mensaje)
            return HttpResponse(status=204)
    
    def post(self,request,opc):
        if request.user.is_authenticated:
            if request.user.action_verify and request.user.verify == False:
                return redirect("../../../../../../../admin/verificar/")
            
            tocken = str(bleach.clean(request.POST.get('tocken'))).strip()
            location = bleach.clean(request.POST.get('location'))
            if "" in [tocken,location]:
                return render(request,f"admin/panel/{location}.html",{
                    "Error":"Todos los campos son obligatorios"
                })
            if tocken != request.user.tocken:
                return render(request,f"admin/panel/{location}.html",{
                    "Error":"Error: Tocken Invalido"
                })

            tocken = utils.get_tocken()
            request.user.tocken = tocken
            request.user.save()
            
            return redirect(f"../../../../../../../../../../../../admin/mfa/{tocken}/")




class MFA(View):
    def get(self, request,tocken):
        if request.user.is_authenticated:
            if request.user.action_verify and request.user.verify == False:
                return redirect("../../../../../../../admin/verificar/")
            
            tocken = bleach.clean(tocken)
            if tocken != request.user.tocken:
                return render(request,f"admin/panel/dashboard.html",{
                    "Error":"Acceso Denegado"
                })
            user = request.user
            device, created = TOTPDevice.objects.get_or_create(user=user, name='default')
            if created:
                device.save()
            qr_code = utils.generate_qr_code(device.config_url)
            request.user.action_verify = True
            request.user.save()
            return render(request, 'admin/panel/setup_2fa.html', {
                'qr_code': qr_code,
                'tocken':tocken
            })
        return redirect("../../../../../../../../../../../../../../../")




class DisableMFA(View):
    def get(self, request, tocken):
        if request.user.is_authenticated:
            if request.user.action_verify and request.user.verify == False:
                return redirect("../../../../../../../admin/verificar/")
            
            tocken = bleach.clean(tocken)
            if tocken != request.user.tocken:
                return render(request, "admin/panel/dashboard.html", {
                    "Error": "Acceso Denegado"
                })
            user = request.user
            try:
                device = TOTPDevice.objects.get(user=user, name='default')
                device.delete()
                request.user.action_verify = False
                request.user.save()
                return render(request, 'admin/panel/setup_2fa.html',{
                    'tocken':tocken
                })
            except TOTPDevice.DoesNotExist:
                return render(request, "admin/panel/setup_2fa.html", {
                    "Error": "No se encontró un dispositivo MFA para deshabilitar",
                    'tocken':tocken
                })
        else:
            return redirect('login')

class RenewMFA(View):
    def get(self, request, tocken):
        if request.user.is_authenticated:
            if request.user.action_verify and request.user.verify == False:
                return redirect("../../../../../../../admin/verificar/")
            
            tocken = bleach.clean(tocken)
            if tocken != request.user.tocken:
                return render(request, "admin/panel/dashboard.html", {
                    "Error": "Acceso Denegado"
                })
            user = request.user
            try:
                device = TOTPDevice.objects.get(user=user, name='default')
                device.delete()
            except TOTPDevice.DoesNotExist:
                pass
            return redirect(f"../../../../../../../../../../admin/mfa/{tocken}/")
        else:
            return redirect('login')



class Verify_2fa(View):
    def get(self,request):
        if request.user.is_authenticated:
            if request.user.action_verify and request.user.verify == False:
                return render(request, 'admin/index/verify_2fa.html')
            return redirect("../../../../../../../../../../../admin/dashboard/")
        return redirect("../../../../../../../../../../../admin/")
        
    
    def post(self,request):
        if request.user.is_authenticated:
            if request.user.action_verify and request.user.verify == False:
                print(request.POST)
                tocken =  bleach.clean(str(request.POST.get('tocken')).strip())
                if v2fa(request=request,user=request.user,tocken=tocken):
                    request.user.verify = True
                    request.user.save()
                    return redirect('../../../../../../../../../../admin/dashboard/')
                else:
                    return render(request, 'admin/index/verify_2fa.html', {'error': 'Error: Tocken Inválido'})
            return redirect("../../../../../../../../../../../admin/dashboard/")
        return redirect("../../../../../../../../../../../admin/")
    



def v2fa(request,user,tocken):
    device = TOTPDevice.objects.get(user=request.user, name='default')
    if device.verify_token(tocken):
        return True
    return False



class Perfil(View):
    def get(self,request):
        pass




'''
regular locations

dashboard


opciones:
    post confirmar email


'''