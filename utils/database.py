from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:B@nk_pa55@192.168.56.3/fastapi_test"
SQLALCHEMY_DATABASE_URL = "postgres://ussdzjzoipnsdc:ef296b13fd776a54458f5fac8469fad3004e962f80cb0e72c0a2451f369a37f3@ec2-63-33-239-176.eu-west-1.compute.amazonaws.com:5432/d4ckhtoedpsmmp"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()