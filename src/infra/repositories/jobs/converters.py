from domain.entities.jobs import JobEntity
from infra.repositories.alchemy_models.jobs import Job as JobDTO


def convert_job_entity_to_dto(job: JobEntity) -> JobDTO:
    return JobDTO(
        id=job.id,
        title=job.title,
        description=job.description,
        salary_from=job.salary_from,
        salary_to=job.salary_to,
        is_active=job.is_active,
        user_id=job.user_id,
    )
