from django.urls import path, include
from .views import UsuariosList
from rest_framework import routers
from .views import LoginView
from .views import RegisterUserView
from .views import UpdateProfile
from .views import UpdateContraseña
from .views import UpdateProgreso
from .views import QuestionListAPIViewAportes
from .views import QuestionListAPIViewCultura
from .views import QuestionListAPIViewHistoria
from .views import getProgreso
from .views import get_valores_historia
from .views import actualizar_valores_historia
from .views import get_valores_cultura
from .views import actualizar_valores_cultura
from .views import get_valores_contribuciones
from .views import actualizar_valores_contribuciones

from rest_framework.documentation import include_docs_urls

router= routers.DefaultRouter()
 #Aplicacion o clase desde donde, vista, nombre
router.register('listaUser', UsuariosList, 'usuarioList1' )


""" Rutas de la aplicación"""
urlpatterns = [
    path('usuario/', include(router.urls)),
    path('docs/', include_docs_urls(title="modulo API")),
    path('login_view/', LoginView.as_view(), name='login_view'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('editProfile/' ,UpdateProfile.as_view(), name='editProfile'),
    path('update_contra/',UpdateContraseña.as_view(), name='update_contra'),
    path('progreso_historia1/',UpdateProgreso.as_view(), name='update_progreso'),
    path('preguntas_aportes/', QuestionListAPIViewAportes.as_view(), name='preguntas_aportes'),
    path('preguntas_cultura/', QuestionListAPIViewCultura.as_view(), name='preguntas_cultura'),
    path('preguntas_historia/', QuestionListAPIViewHistoria.as_view(), name='preguntas_historia'),
    path('get_progreso/',getProgreso.as_view(), name='get_progreso'),
    path('get_valores_historia/', get_valores_historia.as_view(), name='get_valores_historia'),
    path('update_valores_historia/', actualizar_valores_historia.as_view(), name='updata_valores_historia'),
    path('get_valores_cultura/', get_valores_cultura.as_view(), name='get_valores_cultura'),
    path('update_valores_cultura/', actualizar_valores_cultura.as_view(), name='updata_valores_cultura'),
    path('get_valores_contribuciones/', get_valores_contribuciones.as_view(), name='get_valores_contribuciones'),
    path('update_valores_contribuciones/', actualizar_valores_contribuciones.as_view(), name='updata_valores_contribuciones'),
]
