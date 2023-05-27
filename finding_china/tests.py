from django.test import TestCase
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import CustomUser
from django.urls import reverse_lazy
from finding_china.views import RegisterUserView
from rest_framework.authtoken.models import Token
from .serializer import UsuarioSerializer

"""
   Clase RegisterUserViewTestCase

    Esta clase se utiliza para especificar un conjunto de pruebas unitarias y funcionales de los métodos realizados para el desarrollo.

    Atributos:
        None

    Métodos:
        None
"""
class RegisterUserViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    """
    Método de prueba test_register_user_success:

    Objetivo: Verificar que se pueda registrar un usuario con éxito mediante una solicitud POST a la vista RegisterUserView.
    Método: test_register_user_success()
    Resultado esperado: Se espera que la respuesta tenga un código de estado HTTP 200 (OK), indicando que el registro fue exitoso.
    
    """

    def test_register_user_success(self):
        url = reverse_lazy('default:register')

        data = {
            'nombre': 'Test User',
            'email1': 'test2@example.com',
            'contraseña': 'password',
            'foto':"http://imagen.jpg"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Verifica que la respuesta tenga el código de estado correcto

      
        """ Método de prueba test_register_user_invalid_email:
         Objetivo: Verificar que no se pueda registrar un usuario con un correo electrónico inválido mediante una solicitud POST a la vista RegisterUserView.
         Método: test_register_user_invalid_email()
         Resultado esperado: Se espera que la respuesta tenga un código de estado HTTP 404 (NOT FOUND), indicando que la solicitud no se pudo encontrar. Además,
         se espera que no se haya creado el usuario en la base de datos debido al correo electrónico inválido. """
       
      

    def test_register_user_invalid_email(self):
        url = reverse('default:register')  
        data = {
            'nombre': 'Test User',
            'email1': 'invalid_email',
            'contraseña': 'password',
            'foto':"http://imagen.jpg"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # Verifica que la respuesta tenga el código de estado correcto

        # Verifica que no se haya creado el usuario en la base de datos debido al email inválido
        with self.assertRaises(CustomUser.DoesNotExist):
            CustomUser.objects.get(username='testuser')


    def setUp(self):
        self.client = APIClient()
        self.registered_user = self.create_registered_user()  # Crear y guardar el usuario registrado

    def create_registered_user(self):
        # Crear un usuario registrado para utilizar en la prueba de inicio de sesión
        User = CustomUser
        registered_user = User.objects.create_superuser(
            username='Test',
            password='password',
            email='test@example.com',
            profile_picture='http://imagen.jpg'
        )
        return registered_user
    
        """  Método de prueba test_login_with_valid_credentials:
        Objetivo: Verificar que un usuario registrado pueda iniciar sesión correctamente mediante una solicitud POST a la vista de inicio de sesión.
        Método: test_login_with_valid_credentials()
        Resultado esperado: Se espera que la respuesta tenga un código de estado HTTP 200 (OK), indicando que el inicio de sesión fue exitoso. Además,
        se espera que la respuesta contenga un token de acceso y los datos del usuario. """

    def test_login_with_valid_credentials(self):
        url = reverse('default:login_view')
        data = {
            'username': self.registered_user.username,
            'password': 'password',
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)

        # Verificar que la respuesta contenga el token y los datos del usuario
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['valid'], True)

        """Método de prueba test_logout:
           Objetivo: Verificar que un usuario pueda cerrar sesión correctamente mediante una solicitud POST a la vista de cierre de sesión.
           Método: test_logout()
           Resultado esperado: Se espera que la respuesta tenga un código de estado HTTP 200 (OK), indicando que el cierre de sesión fue exitoso.
           Además, se espera que el token de acceso del usuario se haya eliminado."""


    def test_logout(self):
        # Iniciar sesión para obtener un token de acceso válido
        login_url = reverse('default:login_view')
        login_data = {
            'username': self.registered_user.username,
            'password': 'password',
        }
        login_response = self.client.post(login_url, login_data, format='json')
        self.assertEqual(login_response.status_code, 200)
        token = login_response.data['token']

        # Configurar el encabezado de autenticación con el token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        # Llamar a la vista de logout
        logout_url = reverse('logout')
        logout_response = self.client.post(logout_url, {'username': self.registered_user.username}, format='json')
        self.assertEqual(logout_response.status_code, 200)

        # Verificar que el token de acceso del usuario se haya eliminado
        self.assertFalse(Token.objects.filter(user=self.registered_user).exists())

        """Método de prueba test_update_password:

           Objetivo: Verificar que un usuario pueda actualizar su contraseña correctamente mediante una solicitud POST a la vista de actualización de contraseña.
           Método: test_update_password()
           Resultado esperado: Se espera que la respuesta tenga un código de estado HTTP 200 (OK), indicando que la actualización de la contraseña fue exitosa. 
           Además, se espera que la contraseña del usuario se haya actualizado correctamente en la base de datos."""

    def test_update_password(self):
        # Iniciar sesión para obtener un token de acceso válido
        login_url = reverse('default:login_view')
        login_data = {
            'username': self.registered_user.username,
            'password': 'password',
        }
        login_response = self.client.post(login_url, login_data, format='json')
        self.assertEqual(login_response.status_code, 200)
        token = login_response.data['token']

        # Configurar el encabezado de autenticación con el token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        # Llamar a la vista de actualizar contraseña
        update_password_url = reverse('default:update_contra')
        new_password = 'new_password'
        update_password_data = {
            'username': self.registered_user.username,
            'password': new_password,
        }
        update_password_response = self.client.post(update_password_url, update_password_data, format='json')
        self.assertEqual(update_password_response.status_code, 200)

        # Verificar que la contraseña del usuario se haya actualizado correctamente
        updated_user = CustomUser.objects.get(username=self.registered_user.username)
        self.assertTrue(updated_user.check_password(new_password))

        """Método de prueba test_update_profile:

           Objetivo: Verificar que un usuario pueda actualizar su foto de perfil correctamente mediante una solicitud POST a la vista de actualización de foto de perfil.
           Método: test_update_profile()
           Resultado esperado: Se espera que la respuesta tenga un código de estado HTTP 200 (OK), indicando que la actualización de la contraseña fue exitosa. 
           Además, se espera que la foto de perfil nueva coincida con la foto que existe en la base de datos."""

    def test_update_profile(self):
        # Iniciar sesión para obtener un token de acceso válido
        login_url = reverse('default:login_view')
        login_data = {
            'username': self.registered_user.username,
            'password': 'password',
        }
        login_response = self.client.post(login_url, login_data, format='json')
        self.assertEqual(login_response.status_code, 200)
        token = login_response.data['token']

        # Configurar el encabezado de autenticación con el token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        # Llamar a la vista de actualizar foto de perfil
        update_profile_url = reverse('default:editProfile')
        #Se envia una nueva dirección de foto de perfil que contiene una imagen
        new_profile = 'https://img.freepik.com/foto-gratis/elemento-artesania-mano-papel-corazon-rojo_53876-128923.jpg?w=2000'
        update_profile_data = {
            'username': self.registered_user.username,
            'foto': new_profile,
        }
        update_profile_response = self.client.post(update_profile_url, update_profile_data, format='json')
        self.assertEqual(update_profile_response.status_code, 200)

        # Verificar que la imagen del usuario se haya actualizado correctamente
        updated_user = CustomUser.objects.get(username=self.registered_user.username)
        self.assertEqual(updated_user.profile_picture, new_profile)






