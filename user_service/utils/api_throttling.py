# utils/api_throttling.py
import time
from django.core.cache import cache

class APIRateLimiter:
    def __init__(self, api_name, max_requests, period_in_seconds):
        self.api_name = api_name
        self.max_requests = max_requests
        self.period = period_in_seconds
    
    def is_throttled(self, identifier):
        """
        Cek apakah request untuk identifier tertentu sedang di-throttle
        """
        throttle_key = f"throttle_{self.api_name}_{identifier}"
        return cache.get(throttle_key) is not None
    
    def get_retry_after(self, identifier):
        """
        Dapatkan waktu tunggu yang tersisa untuk identifier tertentu
        """
        throttle_key = f"throttle_{self.api_name}_{identifier}"
        throttle_info = cache.get(throttle_key)
        if throttle_info:
            return max(0, throttle_info['wait_until'] - time.time())
        return 0
    
    def record_request(self, identifier):
        """
        Catat request dan cek apakah melebihi batas
        """
        key = f"rate_limit_{self.api_name}_{identifier}"
        current_time = time.time()
        
        # Dapatkan history request
        request_history = cache.get(key, [])
        
        # Hapus request yang sudah lewat period
        request_history = [t for t in request_history if t > current_time - self.period]
        
        # Cek apakah sudah melebihi batas
        if len(request_history) >= self.max_requests:
            # Hitung waktu tunggu
            oldest_request = min(request_history)
            wait_until = oldest_request + self.period
            wait_seconds = wait_until - current_time
            
            # Set throttle info
            throttle_key = f"throttle_{self.api_name}_{identifier}"
            cache.set(
                throttle_key,
                {'wait_until': wait_until},
                timeout=int(wait_seconds) + 10
            )
            
            return wait_seconds
        
        # Tambahkan request saat ini ke history
        request_history.append(current_time)
        cache.set(key, request_history, timeout=self.period)
        
        return 0