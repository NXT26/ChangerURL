import time
import functools
from prometheus_client import Summary, Histogram
import inspect

REQUEST_TIME = Summary(
    'shorten_request_processing_seconds',
    'Time spent processing shorten request')

QR_CODE_GENERATION_TIME = Histogram(
    'qr_code_generation_seconds',
    'Time spent generating QR codes'
)

def track_time(metric):
    def decorator(func):
        if inspect.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                start = time.perf_counter()
                result = await func(*args, **kwargs)
                duration = time.perf_counter() - start
                metric.observe(duration)
                return result
            return async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                start = time.perf_counter()
                result = func(*args, **kwargs)
                duration = time.perf_counter() - start
                metric.observe(duration)
                return result
            return sync_wrapper
    return decorator
