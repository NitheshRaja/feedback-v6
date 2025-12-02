"""
Main API router
"""
from fastapi import APIRouter
from app.api.v1.endpoints import auth, feedback, analysis, reports, users, sync

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(feedback.router, prefix="/feedback", tags=["feedback"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(sync.router, prefix="/sync", tags=["sync"])

