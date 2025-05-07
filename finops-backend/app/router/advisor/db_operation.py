from sqlalchemy.orm import Session
from sqlmodel import delete, select

from core_dependencies.db_operation import DbBase
from router.advisor.schemas import AdvisorModel
from core_dependencies.schemas import Advisor, ExcludedAdvisor


class DbAdvisor(DbBase[Advisor, AdvisorModel, AdvisorModel]):
    def query_by_integration_name(self, db: Session, integration_name: str):
        statement = select(self.model).where(self.model.finops_id == integration_name)
        return db.exec(statement).all()

    def truncate_by_integration_name(self, db: Session, integration_name: str):
        rows = select(self.model).where(self.model.finops_id == integration_name)
        all_rows = db.exec(rows).all()
        for row in all_rows:
            db.delete(row)
        db.commit()

    def truncate_table(self, db: Session):
        return db.exec(delete(self.model))


class DbExcludedAdvisor(DbBase[ExcludedAdvisor, AdvisorModel, AdvisorModel]):
    def query_exclude_advisor_data(
        self, db: Session, recommendation_id: str, integration_name: str
    ):
        statement = (
            select(Advisor)
            .where(Advisor.recommendation_id == recommendation_id)
            .where(Advisor.finops_id == integration_name)
        )

        return db.exec(statement).one_or_none()

    def add_exlude_advisor_data(
        self, db: Session, recommendation_id: str, integration_name: str
    ):
        rows = self.query_exclude_advisor_data(
            db=db,
            recommendation_id=recommendation_id.strip(),
            integration_name=integration_name,
        )

        return self.create(db, rows)

    def delete_by_rec_id(
        self, db: Session, recommendation_id: str, integration_name: str
    ):
        statement = (
            select(self.model)
            .where(self.model.recommendation_id == recommendation_id)
            .where(self.model.finops_id == integration_name)
        )

        row = db.exec(statement).one_or_none()
        return self.delete(db, row.id)

    def query_by_integration_name(self, db: Session, integration_name: str):
        statement = select(self.model).where(self.model.finops_id == integration_name)
        return db.exec(statement).all()


db_advisor = DbAdvisor(Advisor)
db_exclude_advisor = DbExcludedAdvisor(ExcludedAdvisor)