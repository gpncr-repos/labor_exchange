from domain.entities.users import UserEntity
from infra.repositories.alchemy_models.users import User as UserDTO


def convert_user_entity_to_dto(user: UserEntity) -> UserDTO:
    return UserDTO(
        email=user.email,
        name=user.name,
        password=user.password,
        hashed_password=user.hashed_password,
        is_company=user.is_company,
    )
