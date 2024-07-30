from domain.entities.users import UserEntity
from infra.repositories.alchemy_models.users import User as UserDTO


def convert_user_entity_to_dto(user: UserEntity) -> UserDTO:
    return UserDTO(
        id=user.id,
        email=user.email,
        name=user.name,
        hashed_password=user.hashed_password,
        is_company=user.is_company,
    )
