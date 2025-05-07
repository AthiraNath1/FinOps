from typing import Any, Generic, TypeVar, get_args

from sqlalchemy.orm import Query, Session
from sqlmodel import SQLModel

DbModelType = TypeVar("DbModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)


class DbBase(Generic[DbModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[DbModelType]):
        self.model = model

    def query_by_id(self, db: Session, id: Any) -> Query:
        return db.query(self.model).filter(self.model.id == id)

    def query_by(
        self,
        db: Session,
        offset: int = 0,
        limit: int = 5,
        **kwargs,
    ) -> list[DbModelType]:
        return (
            db.query(self.model).filter_by(**kwargs).offset(offset).limit(limit).all()
        )

    def get(self, db: Session, id: Any) -> DbModelType | None:
        return self.query_by_id(db, id).one_or_none()

    def list(
        self,
        db: Session,
    ) -> list[DbModelType]:
        return db.query(self.model).all()

    def create(
        self,
        db: Session,
        object: CreateSchemaType,
        *,
        auto_commit: bool = True,
    ) -> DbModelType:
        db_object = object

        db_type, create_type, _ = get_args(self.__class__.__orig_bases__[0])
        if db_type != create_type:
            db_object = self.model.from_orm(object)

        db.add(db_object)

        if auto_commit:
            db.commit()
            db.refresh(db_object)

        return db_object

    def update(
        self,
        db: Session,
        id: Any,
        update: CreateSchemaType | UpdateSchemaType,
        *,
        auto_commit: bool = True,
        exclude_unset: bool,
    ) -> DbModelType | None:
        fields_to_update = update.dict(exclude_unset=exclude_unset)
        if not fields_to_update:
            return self.get(db, id)

        query = self.query_by_id(db, id)
        row_count = query.update(fields_to_update)

        if auto_commit:
            if row_count != 1:
                db.rollback()
                return None

            db.commit()

        return query.one()

    def delete(
        self,
        db: Session,
        id: Any,
        *,
        auto_commit: bool = True,
    ) -> bool:
        row_count = self.query_by_id(db, id).delete()

        if auto_commit:
            if row_count != 1:
                db.rollback()
                return False

            db.commit()
        return True

    def truncate_table(
        self,
        db: Session,
    ):
        db.query(self.model).delete()
        return db.commit()