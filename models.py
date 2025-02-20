# from sqlalchemy import Column, String
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# class Department(Base):
#     __tablename__ = "department"  # Match this with the actual table name

#     department_id = Column(String(50), primary_key=True, index=True)
#     department_name = Column(String(100), nullable=False)

#     def __repr__(self):
#         return f"<Department(department_id={self.department_id}, department_name={self.department_name})>"

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Department(Base):
    __tablename__ = "department"

    department_id = Column(String(50), primary_key=True, index=True)
    department_name = Column(String(100), nullable=False)

    employees = relationship("Employee", back_populates="department", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Department(department_id={self.department_id}, department_name={self.department_name})>"

class Employee(Base):
    __tablename__ = "employee"

    employee_id = Column(String(50), primary_key=True, index=True)
    employee_name = Column(String(100), nullable=False)
    gender = Column(String(10), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    phone = Column(String(15), nullable=False, unique=True)
    department_id = Column(String(50), ForeignKey("department.department_id", ondelete="SET NULL"))

    department = relationship("Department", back_populates="employees")

    def __repr__(self):
        return f"<Employee(employee_id={self.employee_id}, employee_name={self.employee_name}, email={self.email})>"
