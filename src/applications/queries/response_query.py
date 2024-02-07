"""Сценарии, работающие с таблице откликов responses"""
from sqlalchemy.ext.asyncio import AsyncSession

from applications.command import CommandResult
from domain.do_schemas import DOJob, DOResponse
from infrastructure.repos import RepoResponse, RepoJob
from models import Job, Response
from models import Response as ResponseForVacancy

from api.schemas.response_schema import SResponseForJob





