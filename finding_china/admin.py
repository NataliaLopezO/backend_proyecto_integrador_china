"""
Registro del modelo de usuario personalizado en el panel de administración de Django.

Este fragmento de código registra el modelo de usuario personalizado en el panel de administración de Django.
Permite la administración de usuarios personalizados, incluyendo la creación, edición y eliminación de usuarios,
a través de la interfaz de administración proporcionada por Django.

Importante:
- Este código debe ubicarse en un archivo de configuración de Django, como `admin.py` en la aplicación correspondiente.
- Asegúrese de haber definido previamente un modelo de usuario personalizado en su aplicación.
"""

from django.contrib import admin
from django.contrib.auth import get_user_model

# Obtiene el modelo de usuario personalizado definido en la aplicación
CustomUser = get_user_model()

# Registra el modelo de usuario personalizado en el panel de administración de Django
admin.site.register(CustomUser)
