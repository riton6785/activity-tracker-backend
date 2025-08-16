from .activities_route import router as activity_router
from .user_route import router as user_router
from .project_route import router as project_router
from .task_route import router as task_router

all_routers = [activity_router, user_router, project_router, task_router]
