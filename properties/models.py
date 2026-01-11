"""
Models for the properties app
"""
from django.db import models


class Property(models.Model):
    """
    Property model representing a real estate listing.
    
    Attributes:
        title: The title/name of the property
        description: Detailed description of the property
        price: The listing price
        location: Geographic location of the property
        created_at: Timestamp when the property was listed
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'properties'
        ordering = ['-created_at']
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
    
    def __str__(self):
        return f"{self.title} - {self.location} (${self.price})"
