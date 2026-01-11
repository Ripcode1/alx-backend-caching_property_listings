"""
Django signals for cache invalidation
Automatically invalidates cached data when Property objects are modified
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property
import logging

logger = logging.getLogger('properties')


@receiver(post_save, sender=Property)
def invalidate_property_cache_on_save(sender, instance, created, **kwargs):
    """
    Signal handler to invalidate cache when a Property is created or updated.
    
    Args:
        sender: The model class (Property)
        instance: The actual instance being saved
        created: Boolean indicating if this is a new instance
        **kwargs: Additional keyword arguments
    """
    cache_key = 'all_properties'
    cache.delete(cache_key)
    
    action = "created" if created else "updated"
    logger.info(f"Property {instance.id} {action}. Cache key '{cache_key}' invalidated.")


@receiver(post_delete, sender=Property)
def invalidate_property_cache_on_delete(sender, instance, **kwargs):
    """
    Signal handler to invalidate cache when a Property is deleted.
    
    Args:
        sender: The model class (Property)
        instance: The actual instance being deleted
        **kwargs: Additional keyword arguments
    """
    cache_key = 'all_properties'
    cache.delete(cache_key)
    
    logger.info(f"Property {instance.id} deleted. Cache key '{cache_key}' invalidated.")
