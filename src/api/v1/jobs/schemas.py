from pydantic import BaseModel, Field

from domain.entities.jobs import JobEntity


class JobCreateSchema(BaseModel):
    title: str
    description: str
    salary_from: float
    salary_to: float
    is_active: bool = True
    user_id: str

    def to_entity(self) -> JobEntity:
        return JobEntity(
            title=self.title,
            description=self.description,
            salary_from=self.salary_from,
            salary_to=self.salary_to,
            is_active=self.is_active,
            user_id=self.user_id
        )


class JobSchema(BaseModel):
    id: str
    title: str
    description: str
    salary_from: float
    salary_to: float
    is_active: bool = True
    user_id: str
    responses_ids: list[int] = Field(default_factory=list)

    @classmethod
    def from_entity(cls, entity: JobEntity) -> "JobSchema":
        return JobSchema(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            salary_from=entity.salary_from,
            salary_to=entity.salary_to,
            is_active=entity.is_active,
            user_id=entity.user_id,
            responses_ids=entity.responses_ids,
        )
