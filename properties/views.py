"""
Views for the properties app
Implements view-level caching for property listings
"""
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .utils import get_all_properties


@cache_page(60 * 15)  # Cache for 15 minutes
def property_list(request):
    """
    View to display all properties.
    Response is cached in Redis for 15 minutes using @cache_page decorator.
    
    Returns:
        JsonResponse: List of all properties with their details
    """
    properties = get_all_properties()
    
    # Convert queryset to list of dictionaries
    properties_data = [
        {
            'id': prop.id,
            'title': prop.title,
            'description': prop.description,
            'price': str(prop.price),
            'location': prop.location,
            'created_at': prop.created_at.isoformat(),
        }
        for prop in properties
    ]
    
    return JsonResponse({
        'count': len(properties_data),
        'properties': properties_data
    })
