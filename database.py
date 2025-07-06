from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = 'postgresql://tareas_database_user:1FnooQ1aGawfvF8NabTVhimlJ1SphKc6@dpg-d1kt6p3e5dus73f07gug-a.oregon-postgres.render.com/tareas_database'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()