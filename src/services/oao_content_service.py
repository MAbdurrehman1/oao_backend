from cexceptions import NotFoundException
from entity import OAOContent
from repository import DeepDiveRepository, OAOContentRepository, ParticipationRepository


def get_deep_dive_oao_content_list(
    deep_dive_id: int, offset: int, limit: int
) -> tuple[int, list[OAOContent]]:
    if not DeepDiveRepository.exists(_id=deep_dive_id):
        raise NotFoundException(
            entity="DeepDive",
            arg="ID",
            value=str(deep_dive_id),
        )
    return OAOContentRepository.get_list(
        deep_dive_id=deep_dive_id,
        offset=offset,
        limit=limit,
    )


def view_oao_content(user_id: int, content_id: int) -> None:
    if not OAOContentRepository.exists(_id=content_id):
        raise NotFoundException(
            entity="OAOContent",
            arg="ID",
            value=str(content_id),
        )
    participation_id = ParticipationRepository.get_participation_id_by_user_id(
        user_id=user_id
    )
    OAOContentRepository.upsert_oao_content_view(
        participation_id=participation_id,
        content_id=content_id,
    )


def get_participant_viewed_oao_content_ids_list(user_id: int) -> list[int]:
    participation_id = ParticipationRepository.get_participation_id_by_user_id(
        user_id=user_id,
    )
    return OAOContentRepository.get_viewed_content_ids_list(
        participation_id=participation_id,
    )
