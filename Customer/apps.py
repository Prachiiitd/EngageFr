from django.apps import AppConfig


class CustomerConfig(AppConfig):
    """
    This class is used to configure the application.
    """
    default_auto_field = 'django.db.models.BigAutoField'  # Set the default auto field.
    name = 'Customer'  # Set the name of the application.
