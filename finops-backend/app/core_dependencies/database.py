from collections.abc import Generator
from contextlib import contextmanager
import pyodbc
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, create_engine

from core_dependencies.settings import settings


class Database:
    def __init__(self) -> None:
        self.url = URL.create(
            drivername=settings.db_driver,
            username=settings.db_user,
            password=settings.db_password,
            host=settings.db_host,
            port=settings.db_port,
            database=settings.db_database,
            query={"driver": "ODBC Driver 17 for SQL Server"},
        )
        
        print(f"🔍 Connecting to: {self.url}")  # ✅ Debug: Print connection details
        
        try:
            # Attempt raw connection with pyodbc
            conn_str = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER=tcp:{settings.db_host},1433;"
                f"DATABASE={settings.db_database};"
                f"UID={settings.db_user};"
                f"PWD={settings.db_password};"
                f"Encrypt=yes;"
                f"TrustServerCertificate=no;"
                f"Connection Timeout=30;"
            )
            conn = pyodbc.connect(conn_str)
            print("✅ PyODBC Connection successful!")

        except Exception as e:
            print(f"❌ PyODBC Connection failed: {e}")

        # Attempt SQLAlchemy connection
        try:
            self.engine = create_engine(self.url)
            with self.engine.connect() as connection:
                print("✅ SQLAlchemy Connection successful!")
        except SQLAlchemyError as e:
            print(f"❌ SQLAlchemy Connection failed: {e}")

    @contextmanager
    def session(self, *, autocommit: bool = False) -> Generator[Session, None, None]:
        db = None
        try:
            db = Session(self.engine)
            yield db
            if autocommit:
                db.commit()
        except SQLAlchemyError as e:
            print(f"❌ Database Error: {e}")
            db.rollback()
        finally:
            db.close()


database = Database()


def get_db() -> Generator[Session, None, None]:
    db = Database()
    with db.session() as session:
        yield session
