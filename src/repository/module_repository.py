from copy import deepcopy
from datetime import datetime
from uuid import UUID

from cexceptions import NotFoundException
from entity import Module, File
from settings.connections import postgres_connection_manager
from .queries import (
    GET_MODULES_LIST,
    STORE_MODULE,
    STORE_MODULE_ANSWER,
    GET_LAST_ANSWERED_MODULE_ORDER,
    GET_MODULE_DATA_UNTIL_ORDER,
    CHECK_MODULE_ID_EXISTS,
    CHECK_IS_LAST_MODULE,
    UPDATE_LAST_MODULE_ORDER,
    GET_PARTICIPANT_LAST_MODULE_ORDER,
    UPDATE_MODULE_ANSWER_UPDATED_AT,
)


def _enrich_module(data: dict) -> Module:
    animated_thumbnail = File(
        id=data["animated_thumbnail_id"],
        file_path=data["animated_thumbnail_url"],
    )
    still_thumbnail = File(
        id=data["still_thumbnail_id"],
        file_path=data["still_thumbnail_url"],
    )
    return Module(
        id=data["id"],
        title=data["title"],
        description=data["description"],
        duration=data["duration"],
        order=data["module_order"],
        still_thumbnail=still_thumbnail,
        animated_thumbnail=animated_thumbnail,
        created_at=data["created_at"],
        updated_at=data["updated_at"],
    )


class ModuleRepository:
    connection_manager = postgres_connection_manager

    @classmethod
    def get_list(cls, offset: int, limit: int) -> tuple[int, list[Module]]:
        result = cls.connection_manager.execute_atomic_query_all(
            query=GET_MODULES_LIST,
            variables=(offset, limit),
        )
        if not result:
            return 0, []

        total_count = result[0]["total_count"]
        modules = [_enrich_module(item) for item in result]
        return total_count, modules

    @classmethod
    def store(cls, module: Module) -> Module:
        result = cls.connection_manager.execute_atomic_query(
            query=STORE_MODULE,
            variables=(
                module.title,
                module.description,
                module.duration,
                module.order,
                module.url,
                module.animated_thumbnail_id,
                module.still_thumbnail_id,
            ),
        )
        stored_module = deepcopy(module)
        stored_module.id = result["id"]
        stored_module.created_at = result["created_at"]
        stored_module.updated_at = result["updated_at"]
        return stored_module

    @classmethod
    def store_module_answer(cls, participation_id: UUID, module_id: int):
        cls.connection_manager.execute_atomic_query(
            query=STORE_MODULE_ANSWER,
            variables=(str(participation_id), module_id),
        )

    @classmethod
    def get_last_answered_module_order(cls, participation_id: UUID) -> int:
        result = cls.connection_manager.execute_atomic_query(
            query=GET_LAST_ANSWERED_MODULE_ORDER,
            variables=(str(participation_id),),
        )
        if not result:
            return 0
        return result["module_order"]

    @classmethod
    def get_modules_data_until_order(
        cls, order: int
    ) -> dict[int, dict[str, str | int]]:
        result = cls.connection_manager.execute_atomic_query_all(
            query=GET_MODULE_DATA_UNTIL_ORDER,
            variables=(order,),
        )
        return {
            item["module_order"]: dict(url=item["url"], id=item["id"])
            for item in result
        }

    @classmethod
    def exists(cls, _id: int) -> bool:
        result = cls.connection_manager.execute_atomic_query(
            query=CHECK_MODULE_ID_EXISTS,
            variables=(_id,),
        )
        return result["exists"]

    @classmethod
    def is_last_module(cls, _id: int) -> bool:
        result = cls.connection_manager.execute_atomic_query(
            query=CHECK_IS_LAST_MODULE,
            variables=(_id,),
        )
        return result["is_last_module"]

    @classmethod
    def update_last_order(
        cls,
        participation_id: UUID,
        last_answered_module_order: int,
    ):
        cls.connection_manager.execute_atomic_query(
            query=UPDATE_LAST_MODULE_ORDER,
            variables=(last_answered_module_order, str(participation_id)),
        )

    @classmethod
    def get_last_order(
        cls,
        participation_id: UUID,
    ) -> int:
        result = cls.connection_manager.execute_atomic_query(
            query=GET_PARTICIPANT_LAST_MODULE_ORDER,
            variables=(participation_id,),
        )
        if not result:
            raise NotFoundException(
                entity="Participation",
                arg="ID",
                value=str(participation_id),
            )
        return result["last_answered_module_order"]

    @classmethod
    def update_module_answer_updated_at(
        cls,
        participation_id: UUID,
        module_id: int,
        updated_at: datetime,
    ):
        cls.connection_manager.execute_atomic_query(
            query=UPDATE_MODULE_ANSWER_UPDATED_AT,
            variables=(
                updated_at,
                module_id,
                str(participation_id),
            ),
        )
