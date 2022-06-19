from typing import Generic, Type, TypeVar, cast
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CrudBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, db: AsyncSession, id: UUID) -> ModelType | None:
        """
        Get a single record by id.
        **Parameters**
        * `id`: Record id
        * `db`: SQLAlchemy session
        **Returns**
        * A single record
        #"""
        select_query = select([self.model]).where(self.model.id == id)
        result = await db.execute(select_query)

        return cast(ModelType | None, result.scalar())

    async def get_all(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> list[ModelType]:
        """
        Get all records.
        **Parameters**
        * `db`: SQLAlchemy session
        **Returns**
        * A list of records
        """
        select_query = select([self.model]).offset(skip).limit(limit)
        result = await db.execute(select_query)

        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new record.
        **Parameters**
        * `db`: SQLAlchemy session
        * `obj_in`: Pydantic model (schema)
        **Returns**
        * A new record
        """
        obj_in_data = jsonable_encoder(obj_in)
        result = await db.execute(insert(self.model).values(**obj_in_data))

        if not isinstance(result, CursorResult):
            raise Exception("Could not insert record")

        await db.commit()
        data = await self.get(db, result.inserted_primary_key[0])

        if not data:
            raise Exception("Could not get inserted record")

        return data

    async def update(
        self, db: AsyncSession, id: UUID, *, obj_in: UpdateSchemaType
    ) -> None:
        """
        Update a record.
        **Parameters**
        * `db`: SQLAlchemy session
        * `id`: Record id
        * `obj_in`: Pydantic model (schema)
        **Returns**
        * `returns` A new record
        """
        update_data = obj_in.dict(exclude_unset=True)

        update_query = (
            update(self.model).where(self.model.id == id).values(**update_data)
        )
        await db.execute(update_query)
        await db.commit()

    async def delete(self, db: AsyncSession, *, id: UUID) -> None:
        """
        Delete a record.
        **Parameters**
        * `db`: SQLAlchemy session
        * `id`: Record id
        """
        delete_query = delete(self.model).where(self.model.id == id)
        await db.execute(delete_query)
        await db.commit()
