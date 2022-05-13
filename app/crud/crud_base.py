from typing import Any, Generic, Optional, Type, TypeVar, Union
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.engine import CursorResult
from sqlalchemy.orm import Session

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

    def get(self, db: Session, id: UUID) -> Optional[ModelType]:
        """
        Get a single record by id.
        **Parameters**
        * `id`: Record id
        * `db`: SQLAlchemy session
        **Returns**
        * A single record
        #"""
        select_query = select([self.model]).where(self.model.id == id)
        return db.execute(select_query).scalar()

    def get_all(
        self,
        db: Session,
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
        return db.execute(select_query).scalars().all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new record.
        **Parameters**
        * `db`: SQLAlchemy session
        * `obj_in`: Pydantic model (schema)
        **Returns**
        * A new record
        """
        obj_in_data = jsonable_encoder(obj_in)
        result = db.execute(insert(self.model).values(**obj_in_data))

        if not isinstance(result, CursorResult):
            raise Exception("Could not insert record")

        db.commit()
        data = self.get(db, result.inserted_primary_key[0])

        if not data:
            raise Exception("Could not get inserted record")

        return data

    def update(
        self,
        db: Session,
        id: UUID,
        *,
        obj_in: Union[UpdateSchemaType, dict[str, Any]],
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
        update_data = (
            obj_in if isinstance(obj_in, dict) else obj_in.dict(exclude_unset=True)
        )

        update_query = (
            update(self.model).where(self.model.id == id).values(**update_data)
        )
        db.execute(update_query)
        db.commit()

    def delete(self, db: Session, *, id: UUID) -> None:
        """
        Delete a record.
        **Parameters**
        * `db`: SQLAlchemy session
        * `id`: Record id
        """
        delete_query = delete(self.model).where(self.model.id == id)
        db.execute(delete_query)
        db.commit()
