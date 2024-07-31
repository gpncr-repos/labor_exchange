from domain.entities.responses import ResponseEntity
from infra.repositories.alchemy_models.responses import Response as ResponseDTO


def convert_response_entity_to_dto(response: ResponseEntity) -> ResponseDTO:
    return ResponseDTO(
        id=response.id,
        message=response.message,
        job_id=response.job_id,
        user_id=response.user_id,
    )
