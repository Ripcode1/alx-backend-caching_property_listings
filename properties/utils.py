"""
Utility functions for properties app
Implements low-level caching and cache metrics analysis
"""
from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property
import logging

logger = logging.getLogger('properties')


def get_all_properties():
    """
    Retrieve all properties from cache or database.
    Uses Django's low-level cache API to cache the queryset for 1 hour.
    
    Cache key: 'all_properties'
    Cache timeout: 3600 seconds (1 hour)
    
    Returns:
        QuerySet: All Property objects
    """
    cache_key = 'all_properties'
    
    # Try to get data from cache
    properties = cache.get(cache_key)
    
    if properties is not None:
        logger.info(f"Cache HIT for key: {cache_key}")
        return properties
    
    # Cache miss - fetch from database
    logger.info(f"Cache MISS for key: {cache_key}. Fetching from database...")
    properties = list(Property.objects.all())
    
    # Store in cache for 1 hour (3600 seconds)
    cache.set(cache_key, properties, 3600)
    logger.info(f"Cached {len(properties)} properties for 1 hour")
    
    return properties


def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache performance metrics.
    
    Connects to Redis and retrieves:
    - keyspace_hits: Number of successful key lookups
    - keyspace_misses: Number of failed key lookups
    - hit_ratio: Percentage of successful cache hits
    
    Returns:
        dict: Dictionary containing cache metrics
            {
                'hits': int,
                'misses': int,
                'hit_ratio': float,
                'total_keys': int,
                'memory_used': str
            }
    """
    try:
        # Get Redis connection
        redis_conn = get_redis_connection('default')
        
        # Get Redis INFO stats
        info = redis_conn.info('stats')
        
        # Extract metrics
        hits = info.get('keyspace_hits', 0)
        misses = info.get('keyspace_misses', 0)
        
        # Calculate hit ratio
        total_requests = hits + misses
        hit_ratio = (hits / total_requests * 100) if total_requests > 0 else 0
        
        # Get memory info
        memory_info = redis_conn.info('memory')
        memory_used = memory_info.get('used_memory_human', 'N/A')
        
        # Get total keys
        total_keys = redis_conn.dbsize()
        
        # Prepare metrics dictionary
        metrics = {
            'hits': hits,
            'misses': misses,
            'hit_ratio': round(hit_ratio, 2),
            'total_requests': total_requests,
            'total_keys': total_keys,
            'memory_used': memory_used,
        }
        
        # Log metrics
        logger.info("="*60)
        logger.info("Redis Cache Metrics")
        logger.info("="*60)
        logger.info(f"Cache Hits: {hits}")
        logger.info(f"Cache Misses: {misses}")
        logger.info(f"Total Requests: {total_requests}")
        logger.info(f"Hit Ratio: {hit_ratio:.2f}%")
        logger.info(f"Total Keys in Cache: {total_keys}")
        logger.info(f"Memory Used: {memory_used}")
        logger.info("="*60)
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {str(e)}")
        return {
            'error': str(e),
            'hits': 0,
            'misses': 0,
            'hit_ratio': 0,
            'total_requests': 0,
            'total_keys': 0,
            'memory_used': 'N/A',
        }
