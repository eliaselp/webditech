#from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('',views.Login.as_view()),
    path('dashboard/',views.Panel.as_view()),
    path('logout/',views.Logout),
    path('verificar/',views.Verify_2fa.as_view()),
    path('perfil/',views.Perfil.as_view()),

    path('verificar_mail/<int:opc>/',views.backend_verificacion_email.as_view()),
    path('mfa/<str:tocken>/',views.MFA.as_view()),
    path('disablemfa/<str:tocken>/',views.DisableMFA.as_view()),
    path('renewmfa/<str:tocken>/',views.RenewMFA.as_view())
]
