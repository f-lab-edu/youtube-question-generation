from typing import Annotated

from fastapi import Depends
from pydantic_settings import BaseSettings
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.orm.decl_api import DeclarativeMeta


class RDSSettings(BaseSettings):
    rds_host: str = "localhost"  # RDS 인스턴스의 호스트 주소
    rds_port: int = 3306  # MySQL의 기본 포트는 3306입니다. 다른 포트를 사용하는 경우 변경하세요.
    rds_db: str = "mysql"  # RDS 데이터베이스 이름
    rds_user: str = "mysql"  # RDS 사용자 이름
    rds_password: str = ""  # RDS 사용자 비밀번호

    class Config:
        env_file = ".env"  # 환경 변수를 로드할 파일
        env_file_encoding = "utf-8"  # 파일 인코딩 설정


# SQLAlchemy 엔진 설정
settings = RDSSettings()
# RDS MySQL에 연결하기 위한 URL 생성
DB_URL = (
    f"mysql+pymysql://{settings.rds_user}:{settings.rds_password}"
    f"@{settings.rds_host}:{settings.rds_port}/{settings.rds_db}"
)
# SQLAlchemy 엔진 생성
engine = create_engine(DB_URL)
# 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 모델 기본 클래스 생성
Base: DeclarativeMeta = declarative_base()
target_metadata = Base.metadata


# SQL 모델
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, unique=True, index=True)


# 데이터베이스 세션 사용
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
