from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from settings import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, unique=True, index=True)
    status = Column(String, index=True)
    data = Column(Text)

def create_database():
    Base.metadata.create_all(bind=engine)

def save_task(task_data):
    db = SessionLocal()
    db_task = Task(task_id=task_data["task_id"], status=task_data["status"], data=str(task_data))
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    db.close()

def get_task_result(task_id):
    db = SessionLocal()
    task = db.query(Task).filter(Task.task_id == task_id).first()
    db.close()
    return task.data if task else None
