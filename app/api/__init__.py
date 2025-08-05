from .organizations import router as organizations_router
from .buildings import router as buildings_router
from .activities import router as activities_router

__all__ = ['organizations_router', 'buildings_router', 'activities_router']
