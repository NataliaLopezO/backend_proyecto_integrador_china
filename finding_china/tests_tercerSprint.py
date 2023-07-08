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

""" PRUEBAS UNITARIAS DEL TERCER SPRINT """

"""
   Clase ThirdUserViewTestCase

    Esta clase se utiliza para especificar un conjunto de pruebas unitarias y funcionales de los métodos realizados para el desarrollo.

    Atributos:
        None

    Métodos:
        None
"""

class ThirdUserViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

    
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
    
    """Método de prueba test_register_user_invalid_contra:
         Objetivo: Verificar que no se pueda registrar un usuario con una contraseña menor a 4 digitos mediante una solicitud POST a la vista RegisterUserView.
         Método: test_register_user_invalid_contra()
         Resultado esperado: Se espera que la respuesta tenga un código de estado HTTP 404 (NOT FOUND), indicando que la solicitud no se pudo encontrar. Además,
         se espera que no se haya creado el usuario en la base de datos debido a la contraseña inválida. """
       
      

    def test_register_user_invalid_contra(self):
        url = reverse('default:register')  
        data = {
            'nombre': 'Test User',
            'email1': 'invalid_email',
            'contraseña': 'pass',
            'foto':"http://imagen.jpg"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # Verifica que la respuesta tenga el código de estado correcto

        # Verifica que no se haya creado el usuario en la base de datos debido al email inválido
        with self.assertRaises(CustomUser.DoesNotExist):
            CustomUser.objects.get(username='testuser')
    
    """Método de prueba test_register_password_empty():

           Objetivo: Verificar si usuario esta tratando de crear la contraseña con un campo vacio.
           Método: test_register_password_empty()
           Resultado esperado: Se espera que la respuesta tenga un código de estado HTTP 400 (BAD REQUEST), 
           indicando que el usuario no puede crearse con una contraseña vacia.
           """

    def test_register_password_empty(self):
        url = reverse('default:register')  
        data = {
            'nombre': 'Test User',
            'email1': 'invalid_email',
            'contraseña': '',
            'foto':"http://imagen.jpg"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Verifica que la respuesta tenga el código de estado correcto

        # Verifica que no se haya creado el usuario en la base de datos debido al email inválido
        with self.assertRaises(CustomUser.DoesNotExist):
            CustomUser.objects.get(username='testuser')
        





