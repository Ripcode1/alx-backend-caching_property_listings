"""
App configuration for properties app
Registers signal handlers when the app is ready
"""
from django.apps import AppConfig


class PropertiesConfig(AppConfig):
    """
    Configuration class for the properties app.
    Imports signals when the app is ready to ensure they are registered.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'properties'
    
    def ready(self):
        """
        Override ready() to import signals when Django starts.
        This ensures that signal handlers are registered.
        """
        import properties.signals  # noqa
