from django.shortcuts import render,redirect
from rest_framework import generics
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework import filters
from rest_framework.decorators import api_view

from .serializer import UsuarioSerializer
from .serializer import QuestionSerializer
from rest_framework import viewsets

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from .models import CustomUser
from .models import Question



"""
    Vista de lista de usuarios que proporciona funcionalidades CRUD para el modelo CustomUser.

    Esta clase es una vista basada en conjuntos (ModelViewSet) proporcionada por Django REST Framework.
    Permite realizar operaciones de creación, recuperación, actualización y eliminación en el modelo CustomUser.

    Atributos:
        - queryset (QuerySet): Conjunto de objetos CustomUser disponibles para la vista. Todos los objetos 
                                CustomUser se incluyen en la consulta por defecto.
        - serializer_class (Serializer): Clase de serializador utilizada para serializar y deserializar 
                                        objetos CustomUser.
        - permission_classes (tuple): Tupla de clases de permisos requeridos para acceder a la vista. En este
                                        caso, se requiere autenticación mediante TokenAuthentication.
        - authentication_class (tuple): Tupla de clases de autenticación utilizadas para autenticar las 7
                                        solicitudes a la vista. En este caso, se utiliza TokenAuthentication.

    Métodos:
        None

    Ejemplo de uso:

    # Configurar las rutas de URL en las URLs de Django

    from rest_framework import routers

    router = routers.DefaultRouter()
    router.register('usuarios', UsuariosList)

    urlpatterns = [
        # ...
        path('api/', include(router.urls)),
        # ...
    ]

    # Ahora se pueden realizar solicitudes CRUD a la URL 'api/usuarios' para interactuar con los usuarios.
"""

class UsuariosList(viewsets.ModelViewSet):

    queryset = CustomUser.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = (IsAuthenticated,)
    authentication_class = (TokenAuthentication,)


"""
    Vista de inicio de sesión de usuario.

    Esta clase es una vista basada en formulario (FormView) proporcionada por Django.
    Permite a los usuarios iniciar sesión utilizando un formulario de autenticación (AuthenticationForm) y 
    redirecciona a una URL de éxito después del inicio de sesión.

    Atributos:
        - template_name (str): Nombre del archivo de plantilla HTML utilizado para renderizar la vista de 
                            inicio de sesión.
        - form_class (Form): Clase de formulario utilizada para manejar el inicio de sesión del usuario. 
                            En este caso, se utiliza AuthenticationForm.
        - success_url (str): URL a la que se redirecciona después del inicio de sesión exitoso.

    Métodos:
        - dispatch(request, *args, **kwargs): Método decorado que maneja la distribución de la solicitud a
                                                la vista. Verifica si el usuario ya está autenticado y 
                                                redirecciona en consecuencia.
        - form_valid(form): Método que se llama cuando el formulario es válido. Autentica al usuario, crea o 
                            recupera un token de autenticación y realiza el inicio de sesión.

    Ejemplo de uso:

    # Configurar las rutas de URL en las URLs de Django

    urlpatterns = [
        # ...
        path('login/', Login.as_view(), name='login'),
        # ...
    ]

    # La URL '/login/' mostrará la vista de inicio de sesión y permitirá a los usuarios iniciar sesión.

"""

class Login(FormView):
    template_name = "login_user.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy('default:usuarioList1-list')

    """
        Método decorado que maneja la distribución de la solicitud a la vista.
        Verifica si el usuario ya está autenticado y redirecciona en consecuencia.

        Parámetros:
            - request (HttpRequest): Objeto de solicitud HTTP.
            - *args: Argumentos posicionales adicionales.
            - **kwargs: Argumentos con nombre adicionales.

        Retorna:
            - HttpResponseRedirect: Objeto de respuesta HTTP de redirección si el usuario está autenticado.
            - super().dispatch(request, *args, **kwargs): Llamada al método de distribución de la vista 
                                                        padre si el usuario no está autenticado.
    """

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login,self).dispatch(request,*args,*kwargs)

    """
        Método que se llama cuando el formulario es válido.
        Autentica al usuario, crea o recupera un token de autenticación y realiza el inicio de sesión.

        Parámetros:
            - form (Form): Objeto de formulario validado.

        Retorna:
            - super().form_valid(form): Llamada al método form_valid de la vista padre.
    """
    def form_valid(self,form):
        user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
        token,_ = Token.objects.get_or_create(user = user)
        if token:
            login(self.request, form.get_user())
            return super(Login,self).form_valid(form)
"""
    Vista para cerrar la sesión de un usuario.

    Esta clase es una vista basada en clase (APIView) proporcionada por Django REST Framework.
    Permite a un usuario cerrar sesión enviando una solicitud POST con el nombre de usuario.

    Métodos:
        - post(request, format=None): Método que maneja la solicitud POST para cerrar la sesión de un usuario.

    Ejemplo de uso:

    # Configurar las rutas de URL en las URLs de Django

    urlpatterns = [
        # ...
        path('logout/', Logout.as_view(), name='logout'),
        # ...
    ]

    # La URL '/logout/' permite a los usuarios cerrar sesión enviando una solicitud POST con el nombre de usuario.
"""
       
class Logout(APIView):
    """
        Método que maneja la solicitud POST para cerrar la sesión de un usuario.

        Parámetros:
            - request (Request): Objeto de solicitud HTTP.
            - format (str): Formato de respuesta deseado. No se utiliza en este caso.

        Retorna:
            - Response: Objeto de respuesta HTTP con estado 200 si el cierre de sesión es exitoso.
            - Response: Objeto de respuesta HTTP con estado 404 si no se encuentra el usuario.
    """
    def post(self, request, format=None):
        username = request.data.get('username')

        try:
            # Buscar al usuario por nombre de usuario en la base de datos
            user = CustomUser.objects.get(username=username)
            
            # Eliminar el token de acceso del usuario
            Token.objects.filter(user=user).delete()
            
            return Response(status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

"""
    Vista para actualizar el perfil de un usuario.

    Esta clase es una vista basada en clase (APIView) proporcionada por Django REST Framework.
    Permite a un usuario actualizar su perfil enviando una solicitud POST con el nombre de usuario y la foto 
    de perfil.

    Métodos:
        - post(request): Método que maneja la solicitud POST para actualizar el perfil de un usuario.

    Ejemplo de uso:

    # Configurar las rutas de URL en las URLs de Django

    urlpatterns = [
        # ...
        path('update-profile/', UpdateProfile.as_view(), name='update-profile'),
        # ...
    ]

    # La URL '/update-profile/' permite a los usuarios actualizar su perfil enviando una solicitud POST con 
    el nombre de usuario y la foto de perfil.
    
"""

class UpdateProfile(APIView):

    """
        Método que maneja la solicitud POST para actualizar el perfil de un usuario.

        Parámetros:
            - request (Request): Objeto de solicitud HTTP.

        Retorna:
            - Response: Objeto de respuesta HTTP con estado 200 si la actualización del perfil es exitosa.
            - Response: Objeto de respuesta HTTP con estado 404 si no se encuentra el usuario o no se encuentra el token asociado.
    """    
    def post(self, request):
        username= request.data.get('username')
        profile= request.data.get('foto')
        
        try:
            # Buscar al usuario por nombre de usuario en la base de datos
            user = CustomUser.objects.get(username=username)
            token_exists = Token.objects.filter(user=user).exists()

            if token_exists:
                user.profile_picture=profile
                user.save()
                return Response(status=status.HTTP_200_OK)
            else:
                # El token no está asociado al usuario
                return Response(status=status.HTTP_404_NOT_FOUND)


        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
"""
    Vista para actualizar la contraseña de un usuario.

    Esta clase es una vista basada en clase (APIView) proporcionada por Django REST Framework.
    Permite a un usuario actualizar su contraseña enviando una solicitud POST con el nombre de usuario y la nueva contraseña.

    Métodos:
        - post(request): Método que maneja la solicitud POST para actualizar la contraseña de un usuario.

    Ejemplo de uso:

    # Configurar las rutas de URL en las URLs de Django

    urlpatterns = [
        # ...
        path('update-contraseña/', UpdateContraseña.as_view(), name='update-contraseña'),
        # ...
    ]

    # La URL '/update-contraseña/' permite a los usuarios actualizar su contraseña enviando una solicitud POST con el nombre de usuario y la nueva contraseña.
"""
class UpdateContraseña(APIView):
    """
        Método que maneja la solicitud POST para actualizar la contraseña de un usuario.

        Parámetros:
            - request (Request): Objeto de solicitud HTTP.

        Retorna:
            - Response: Objeto de respuesta HTTP con estado 200 si la actualización de la contraseña es exitosa.
            - Response: Objeto de respuesta HTTP con estado 404 si no se encuentra el usuario o no se encuentra el token asociado.
            - Response: Objeto de respuesta HTTP con estado 400 si la contraseña no cumple con los requisitos plateados"""
    
    def post(self, request):
        username= request.data.get('username')
        password= request.data.get('password')
        
        try:
            # Buscar al usuario por nombre de usuario en la base de datos
            user = CustomUser.objects.get(username=username)

            token_exists = Token.objects.filter(user=user).exists()

            if password=='' or password==' ' or len(password) < 4:
                return Response(status=status.HTTP_400_BAD_REQUEST)


            if token_exists:
                user.set_password(password)
                user.save()
                return Response(status=status.HTTP_200_OK)
            else:
                # El token no está asociado al usuario
                return Response(status=status.HTTP_404_NOT_FOUND)


        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

"""
    Vista para iniciar sesión de un usuario.

    Esta clase es una vista basada en clase (APIView) proporcionada por Django REST Framework.
    Permite a un usuario iniciar sesión enviando una solicitud POST con el nombre de usuario y la contraseña.

    Métodos:
        - post(request): Método que maneja la solicitud POST para iniciar sesión de un usuario.

    Ejemplo de uso:

    # Configurar las rutas de URL en las URLs de Django

    urlpatterns = [
        # ...
        path('login/', LoginView.as_view(), name='login'),
        # ...
    ]

    # La URL '/login/' permite a los usuarios iniciar sesión enviando una solicitud POST con el nombre de usuario y la contraseña.
"""   

class LoginView(APIView):
    """
        Método que maneja la solicitud POST para iniciar sesión de un usuario.

        Parámetros:
            - request (Request): Objeto de solicitud HTTP.

        Retorna:
            - Response: Objeto de respuesta HTTP con estado 200 si el inicio de sesión es exitoso.
              Contiene el token de autenticación y los datos del usuario autenticado.
            - Response: Objeto de respuesta HTTP con estado 400 si las credenciales proporcionadas son inválidas.
    """
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            # Buscar al usuario por cédula en la base de datos
            usuario = CustomUser.objects.get(username=username)

            # Verificar la contraseña del usuario
            if usuario.check_password(password):
                # Autenticar al usuario y generar un token de autenticación
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    token, _ = Token.objects.get_or_create(user=user)

        

                    user_data = {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'profile_picture': user.profile_picture.url if user.profile_picture else None,
                        # Agrega más campos de información del usuario si es necesario
                    }

                    print(user_data)
                  
                
                    return Response({'valid': True, 'token': token.key, 'user': user_data})

        except CustomUser.DoesNotExist:
            raise AuthenticationFailed('Las credenciales proporcionadas son inválidas.')

        return Response({'valid': False})
    

"""
    Vista para registrar un nuevo usuario.

    Esta clase es una vista basada en clase (APIView) proporcionada por Django REST Framework.
    Permite a un usuario registrarse enviando una solicitud POST con los datos del usuario.

    Métodos:
        - post(request): Método que maneja la solicitud POST para registrar un nuevo usuario.

    Ejemplo de uso:

    # Configurar las rutas de URL en las URLs de Django

    urlpatterns = [
        # ...
        path('register/', RegisterUserView.as_view(), name='register'),
        # ...
    ]

    # La URL '/register/' permite a los usuarios registrarse enviando una solicitud POST con los datos del usuario.
"""    
class RegisterUserView(APIView):
    permission_classes = [AllowAny]  # Permite el acceso sin autenticación
    authentication_classes = []  # No se requiere autenticación
    """
        Método que maneja la solicitud POST para registrar un nuevo usuario.

        Parámetros:
            - request (Request): Objeto de solicitud HTTP.

        Retorna:
            - Response: Objeto de respuesta HTTP con estado 200 si el registro es exitoso.
            - Response: Objeto de respuesta HTTP con estado 404 si ocurre algún error en el registro.
    """
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        foto=  request.data.get("foto") 
        username= request.data.get('nombre')
        email= request.data.get('email1')
        password= request.data.get('contraseña')

        if password=='' or password==' ' or len(password) < 4:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            try:
                validate_email(email)
            except ValidationError:
                return Response(status=status.HTTP_404_NOT_FOUND)
                 

            superuser = CustomUser.objects.create_superuser(
                    username=username,
                    password=password,
                    email=email,
                    profile_picture=foto
        )
        
                #user = CustomUser.objects.create_superuser(**serializer.validated_data)
            superuser.is_staff = True
            superuser.is_superuser = True
         
            return Response(status=status.HTTP_200_OK)
        except:
             return Response(status=status.HTTP_404_NOT_FOUND)
        
    """
    UpdateProgreso: 

    Vista de la API para actualizar el progreso de un usuario en una categoría específica.

    Esta clase define una vista de la API que permite actualizar el progreso de un usuario en una categoría específica.
    El progreso se actualiza mediante una solicitud POST que incluye el nombre de usuario, la categoría y el identificador.

    Métodos:
    - post: Actualiza el progreso del usuario en la categoría especificada según el identificador.

    Parámetros de la solicitud POST:
    - nombre (str): Nombre de usuario del usuario.
    - categoria (str): Categoría en la que se actualiza el progreso.
    - identificador (str): Identificador de la categoría ('historia', 'cultura', 'contribuciones').

    Respuestas:
    - 202 ACCEPTED: Se devuelve si la categoría es 'None' o None.
    - 200 OK: Se devuelve si el progreso se actualiza correctamente.
    - 401 UNAUTHORIZED: Se devuelve si no se encuentra un token de autenticación válido para el usuario.
    """

class UpdateProgreso(APIView):
    
    def post(self, request):
        username= request.data.get('nombre')
        categoria= request.data.get('categoria')
        identificador=request.data.get('identificador')

        
        # Buscar al usuario por nombre de usuario en la base de datos
        user = CustomUser.objects.get(username=username)
        token_exists = Token.objects.filter(user=user).exists()
   

        if token_exists:

            if categoria=='None':
                return Response(status=status.HTTP_202_ACCEPTED)
            
            if categoria==None:
                return Response(status=status.HTTP_202_ACCEPTED)
             
            if identificador=='historia':
                if user.progreso_historia[categoria]==0:
                    user.progreso_historia[categoria]=1
                    print(user.progreso_historia[categoria])
                    user.save()
                print(user.progreso_historia)
                return Response(status=status.HTTP_200_OK)

            
            if identificador=='cultura':
                if user.progreso_cultura[categoria]==0:
                    user.progreso_cultura[categoria]=1
                    print(user.progreso_cultura[categoria])
                    user.save()
                print(user.progreso_cultura)
                return Response(status=status.HTTP_200_OK)
            
            if identificador=='contribuciones':
                if user.progreso_contribuciones[categoria]==0:
                    user.progreso_contribuciones[categoria]=1
                    print(user.progreso_contribuciones[categoria])
                    user.save()
                print(user.progreso_contribuciones)
                return Response(status=status.HTTP_200_OK)

            return Response(status=status.HTTP_200_OK)

            
       
            
        return Response(status=status.HTTP_401_UNAUTHORIZED)

"""
     Vista de la API para obtener una lista de preguntas de la categoría 'aportes'.

    Esta clase define una vista de la API que permite obtener una lista de preguntas de la categoría 'aportes'.
    Las preguntas se obtienen a través de una solicitud GET a esta vista.

    Atributos:
    - queryset: Consulta que obtiene las preguntas de la categoría 'aportes'.
    - serializer_class: Clase de serializador utilizada para serializar las preguntas.
    - filter_backends: Lista de filtros utilizados para ordenar las preguntas.

    """
class QuestionListAPIViewAportes(generics.ListAPIView):
    queryset = Question.objects.filter(categoria='aportes')
    serializer_class = QuestionSerializer
    filter_backends = [filters.OrderingFilter]

    """
    Vista de la API para obtener una lista de preguntas de la categoría 'cultura'.

    Esta clase define una vista de la API que permite obtener una lista de preguntas de la categoría 'cultura'.
    Las preguntas se obtienen a través de una solicitud GET a esta vista.

    Atributos:
    - queryset: Consulta que obtiene las preguntas de la categoría 'cultura'.
    - serializer_class: Clase de serializador utilizada para serializar las preguntas.
    - filter_backends: Lista de filtros utilizados para ordenar las preguntas.
    """

class QuestionListAPIViewCultura(generics.ListAPIView):
    queryset = Question.objects.filter(categoria='cultura')
    serializer_class = QuestionSerializer
    filter_backends = [filters.OrderingFilter]


    """
    Vista de la API para obtener una lista de preguntas de la categoría 'historia'.

    Esta clase define una vista de la API que permite obtener una lista de preguntas de la categoría 'historia'.
    Las preguntas se obtienen a través de una solicitud GET a esta vista.

    Atributos:
    - queryset: Consulta que obtiene las preguntas de la categoría 'historia'.
    - serializer_class: Clase de serializador utilizada para serializar las preguntas.
    - filter_backends: Lista de filtros utilizados para ordenar las preguntas.

    Importante:
    - Asegúrese de tener configurada la ruta adecuada en las URL para acceder a esta vista.
    - El modelo Question y el serializador QuestionSerializer deben estar definidos correctamente en el proyecto.
    """

class QuestionListAPIViewHistoria(generics.ListAPIView):
    queryset = Question.objects.filter(categoria='historia')
    serializer_class = QuestionSerializer
    filter_backends = [filters.OrderingFilter]


"""

    Vista de la API para obtener el progreso de un usuario en diferentes categorías.

    Esta clase define una vista de la API que permite obtener el progreso de un usuario en diferentes categorías.
    El progreso se obtiene mediante una solicitud POST que incluye el nombre de usuario.

    Métodos:
    - post: Obtiene el progreso del usuario en las categorías 'historia', 'cultura' y 'contribuciones'.

    Parámetros de la solicitud POST:
    - username (str): Nombre de usuario del usuario.

    Respuesta:
    - 200 OK: Devuelve un diccionario con el progreso del usuario en las categorías 'historia', 'cultura' y 'contribuciones'.

"""
class getProgreso(APIView):
    def post(self, request):
        # Obtener todos los usuarios de la base de datos
        username = request.data.get('username')  
        user = CustomUser.objects.get(username=username)

        progresos = {
             'historia': user.progreso_historia,    
             'cultura': user.progreso_cultura,
             'contribuciones': user.progreso_contribuciones,
        }
        

        return Response(progresos, status=status.HTTP_200_OK)

#obtener y actualizar aciertos y fallos de el modulo historia 

"""
    Vista de la API para obtener los valores de aciertos y fallos en la categoría 'historia' de un usuario.

    Esta clase define una vista de la API que permite obtener los valores de aciertos y fallos en la categoría 'historia' de un usuario.
    Los valores se obtienen mediante una solicitud POST que incluye el nombre de usuario.

    Métodos:
    - post: Obtiene los valores de aciertos y fallos en la categoría 'historia' de un usuario.

    Parámetros de la solicitud POST:
    - username (str): Nombre de usuario del usuario.

    Respuesta:
    - 200 OK: Devuelve un diccionario con los valores de aciertos y fallos en la categoría 'historia'.
"""

class get_valores_historia(APIView):
    def post(self, request):
        username = request.data.get('username')  
        user = CustomUser.objects.get(username=username)
        
        data = {
                'aciertos_historia': user.aciertos_historia,
                'fallos_historia': user.fallos_historia
        }
        return Response(data, status=status.HTTP_200_OK )

"""
    Vista de la API para actualizar los valores de aciertos y fallos en la categoría 'historia' de un usuario.

    Esta clase define una vista de la API que permite actualizar los valores de aciertos y fallos en la categoría 'historia' de un usuario.
    Los valores se actualizan mediante una solicitud POST que incluye el nombre de usuario, los nuevos valores de aciertos y fallos.

    Métodos:
    - post: Actualiza los valores de aciertos y fallos en la categoría 'historia' de un usuario.

    Parámetros de la solicitud POST:
    - username (str): Nombre de usuario del usuario.
    - aciertos_historia (int): Nuevos valores de aciertos en la categoría 'historia'.
    - fallos_historia (int): Nuevos valores de fallos en la categoría 'historia'.

    Respuestas:
    - 200 OK: Devuelve si los valores se actualizan correctamente.
    - 401 UNAUTHORIZED: Devuelve si no se encuentra un token de autenticación válido para el usuario.

"""
class actualizar_valores_historia(APIView):
    def post(self, request):
        username = request.data.get('username')
        user = CustomUser.objects.get(username=username)
        token_exists = Token.objects.filter(user=user).exists()
        if token_exists:

            aciertos = int(request.data.get('aciertos_historia'))
            fallos = int(request.data.get('fallos_historia'))
            if aciertos is not None:
                user.aciertos_historia = aciertos
            if fallos is not None:
                user.fallos_historia = fallos
            user.save()
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_401_UNAUTHORIZED)
    

#obtener y actualizar aciertos y fallos de el modulo cultura 
"""
    Vista de la API para obtener los valores de aciertos y fallos en la categoría 'cultura' de un usuario.

    Esta clase define una vista de la API que permite obtener los valores de aciertos y fallos en la categoría 'cultura' de un usuario.
    Los valores se obtienen mediante una solicitud POST que incluye el nombre de usuario.

    Métodos:
    - post: Obtiene los valores de aciertos y fallos en la categoría 'cultura' de un usuario.

    Parámetros de la solicitud POST:
    - username (str): Nombre de usuario del usuario.

    Respuesta:
    - 200 OK: Devuelve un diccionario con los valores de aciertos y fallos en la categoría 'cultura'.
"""

class get_valores_cultura(APIView):
    def post(self, request):
        username = request.data.get('username')  
        user = CustomUser.objects.get(username=username)
        
        data = {
                'aciertos_cultura': user.aciertos_cultura,
                'fallos_cultura': user.fallos_cultura
        }
        return Response(data, status=status.HTTP_200_OK )
    
"""
    Vista de la API para actualizar los valores de aciertos y fallos en la categoría 'Cultura' de un usuario.

    Esta clase define una vista de la API que permite actualizar los valores de aciertos y fallos en la categoría 'Cultura' de un usuario.
    Los valores se actualizan mediante una solicitud POST que incluye el nombre de usuario, los nuevos valores de aciertos y fallos.

    Métodos:
    - post: Actualiza los valores de aciertos y fallos en la categoría 'Cultura' de un usuario.

    Parámetros de la solicitud POST:
    - username (str): Nombre de usuario del usuario.
    - aciertos_cultura (int): Nuevos valores de aciertos en la categoría 'Cultura'.
    - fallos_cultura (int): Nuevos valores de fallos en la categoría 'Cultura'.

    Respuestas:
    - 200 OK: Devuelve si los valores se actualizan correctamente.
    - 401 UNAUTHORIZED: Devuelve si no se encuentra un token de autenticación válido para el usuario.

"""

class actualizar_valores_cultura(APIView):
    def post(self, request):
        username = request.data.get('username')
        user = CustomUser.objects.get(username=username)
        token_exists = Token.objects.filter(user=user).exists()
        if token_exists:

            aciertos = int(request.data.get('aciertos_cultura'))
            fallos = int(request.data.get('fallos_cultura'))
            if aciertos is not None:
                user.aciertos_cultura = aciertos
            if fallos is not None:
                user.fallos_cultura = fallos
            user.save()
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
#obtener y actualizar aciertos y fallos de el modulo aportes

"""
    Vista de la API para obtener los valores de aciertos y fallos en la categoría 'Contribuciones' de un usuario.

    Esta clase define una vista de la API que permite obtener los valores de aciertos y fallos en la categoría 'Contribuciones' de un usuario.
    Los valores se obtienen mediante una solicitud POST que incluye el nombre de usuario.

    Métodos:
    - post: Obtiene los valores de aciertos y fallos en la categoría 'Contribuciones' de un usuario.

    Parámetros de la solicitud POST:
    - username (str): Nombre de usuario del usuario.

    Respuesta:
    - 200 OK: Devuelve un diccionario con los valores de aciertos y fallos en la categoría 'Contribuciones'.
"""

class get_valores_contribuciones(APIView):
    def post(self, request):
        username = request.data.get('username')  
        user = CustomUser.objects.get(username=username)
        
        data = {
                'aciertos_contribuciones': user.aciertos_contribuciones,
                'fallos_contribuciones': user.fallos_contribuciones
        }
        return Response(data, status=status.HTTP_200_OK )
    
"""
    Vista de la API para actualizar los valores de aciertos y fallos en la categoría 'Contribuciones' de un usuario.

    Esta clase define una vista de la API que permite actualizar los valores de aciertos y fallos en la categoría 'Contribuciones' de un usuario.
    Los valores se actualizan mediante una solicitud POST que incluye el nombre de usuario, los nuevos valores de aciertos y fallos.

    Métodos:
    - post: Actualiza los valores de aciertos y fallos en la categoría 'Contribuciones' de un usuario.

    Parámetros de la solicitud POST:
    - username (str): Nombre de usuario del usuario.
    - aciertos_contribuciones (int): Nuevos valores de aciertos en la categoría 'Contribuciones'.
    - fallos_contribuciones (int): Nuevos valores de fallos en la categoría 'Contribuciones'.

    Respuestas:
    - 200 OK: Devuelve si los valores se actualizan correctamente.
    - 401 UNAUTHORIZED: Devuelve si no se encuentra un token de autenticación válido para el usuario.

"""

class actualizar_valores_contribuciones(APIView):
    def post(self, request):
        username = request.data.get('username')
        user = CustomUser.objects.get(username=username)
        token_exists = Token.objects.filter(user=user).exists()
        if token_exists:

            aciertos = int(request.data.get('aciertos_contribuciones'))
            fallos = int(request.data.get('fallos_contribuciones'))
            if aciertos is not None:
                user.aciertos_contribuciones = aciertos
            if fallos is not None:
                user.fallos_contribuciones = fallos
            user.save()
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_401_UNAUTHORIZED)