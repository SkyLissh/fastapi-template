from typing import Generic, Sequence, Type, TypeVar
from uuid import UUID

from app.db.base_class import Base
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

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
        select_query = select(self.model).where(self.model.id == id)
        return (await db.scalars(select_query)).first()

    async def get_all(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[ModelType]:
        """
        Get all records.
        **Parameters**
        * `db`: SQLAlchemy session
        **Returns**
        * A list of records
        """
        select_query = select(self.model).limit(limit).offset(skip)
        return (await db.scalars(select_query)).all()

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
        result = await db.scalar(
            insert(self.model).values(**obj_in_data).returning(self.model)
        )
        await db.commit()

        if not result:
            raise Exception("Could not insert record")

        return result

    async def update(
        self, db: AsyncSession, id: UUID, *, obj_in: UpdateSchemaType
    ) -> ModelType:
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
            update(self.model)
            .where(self.model.id == id)
            .values(**update_data)
            .returning(self.model)
        )
        result = await db.scalar(update_query)

        if not result:
            raise Exception("Could not update record")

        return result

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
