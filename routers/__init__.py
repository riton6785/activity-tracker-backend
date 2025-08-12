from .activities_route import router as activity_router
from .user_route import router as user_router

all_routers = [activity_router, user_router]

