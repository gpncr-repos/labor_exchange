from fixtures.jobs import JobFactory
from fixtures.responses import ResponseFactory
from fixtures.users import UserFactory


class Conveyor:
    @staticmethod
    async def create_emploer(sa_session) -> UserFactory:
        emploer = UserFactory.build()
        emploer.is_company = True
        sa_session.add(emploer)
        sa_session.flush()
        return emploer

    @staticmethod
    async def create_woker(sa_session) -> UserFactory:
        woker = UserFactory.build()
        woker.is_company = True
        sa_session.add(woker)
        sa_session.flush()
        return woker

    @staticmethod
    async def current_to_company(sa_session, current_user: UserFactory) -> UserFactory:
        current_user.is_company = True
        sa_session.add(current_user)
        sa_session.flush()
        return current_user

    @staticmethod
    async def current_to_worker(sa_session, current_user: UserFactory) -> UserFactory:
        current_user.is_company = False
        sa_session.add(current_user)
        sa_session.flush()
        return current_user

    @staticmethod
    async def create_job(sa_session, current_user: UserFactory) -> JobFactory:
        job = JobFactory.build()
        job.user_id = current_user.id
        job.is_active = True
        sa_session.add(job)
        sa_session.flush()
        return job

    @staticmethod
    async def create_response(sa_session, user: UserFactory, job: JobFactory) -> ResponseFactory:
        response = ResponseFactory.build()
        response.job_id = job.id
        response.user_id = user.id
        sa_session.add(response)
        sa_session.flush()
        return response

    @staticmethod
    async def job_to_not_active(sa_session, job):
        job.is_active = False
        sa_session.add(job)
        sa_session.flush()
        return job
