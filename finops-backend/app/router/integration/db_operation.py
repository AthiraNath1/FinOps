from sqlmodel import Session, select

from core_dependencies.db_operation import DbBase
from router.integration.schemas import (
    IntegrationCreateModel,
    IntegrationUpdateModel,
    PlatformType,
)
from core_dependencies.schemas import Integration


class DBIntegration(
    DbBase[Integration, IntegrationCreateModel, IntegrationUpdateModel]
):
    def get_by_name(self, integration_name: str, db: Session):
        statement = select(self.model).where(
            self.model.integration_name == integration_name
        )
        return db.exec(statement=statement).one_or_none()

    def list_by_user(self, db: Session, user_email: str, platform: PlatformType):
        statement = (
            select(self.model)
            .where(self.model.user_email == user_email)
            .where(self.model.platform == platform)
        )
        return db.exec(statement=statement).all()
    
    def get_user(self, db: Session, user_email: str):
        statement = (
            select(self.model)
            .where(self.model.user_email == user_email)
        )
        return db.exec(statement=statement).all()
    
    def delete_by_name(self, integration_name: str, db: Session):
        data = self.get_by_name(integration_name=integration_name, db=db)
        return self.delete(db=db, id=data.id)


db_integration = DBIntegration(Integration)