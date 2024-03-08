## CProfiler
import cProfile
import io
import pstats
from starlette.middleware.base import BaseHTTPMiddleware


class CProfileMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        profiler = cProfile.Profile()
        profiler.enable()
        response = await call_next(request)
        profiler.disable()
        stream = io.StringIO()
        stats = pstats.Stats(profiler, stream=stream)
        stats.strip_dirs().sort_stats('cumulative').print_stats(20)
        print(stream.getvalue())  # You can log or display this information as needed
        return response
