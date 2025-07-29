from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://todo_jx70_user:xwWjBrxsw5L672In3hHbr1wP28v8sl6D@dpg-d24a29p5pdvs7383o35g-a.oregon-postgres.render.com/todo_jx70"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
