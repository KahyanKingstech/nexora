from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Department(Base):
    __tablename__ = "department"  # Match this with the actual table name

    department_id = Column(String(50), primary_key=True, index=True)
    department_name = Column(String(100), nullable=False)

    def __repr__(self):
        return f"<Department(department_id={self.department_id}, department_name={self.department_name})>"
