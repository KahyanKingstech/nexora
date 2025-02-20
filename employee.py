from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import get_db_connection

router = APIRouter()

# ✅ Define Employee Request Model
class EmployeeCreate(BaseModel):
    employee_id: str
    employee_name: str
    gender: str
    email: str
    phone: str
    department_id: str

class EmployeeUpdate(BaseModel):
    employee_name: str
    gender: str
    email: str
    phone: str
    department_id: str

# ✅ GET - Retrieve all employees
@router.get("/api/employees")
async def get_employees():
    conn = await get_db_connection()
    async with conn.cursor() as cursor:
        await cursor.execute("SELECT employee_id, employee_name, gender, email, phone, department_id FROM employee")
        result = await cursor.fetchall()
    
    await conn.ensure_closed()
    
    employees = [
        {
            "employee_id": row[0],
            "employee_name": row[1],
            "gender": row[2],
            "email": row[3],
            "phone": row[4],
            "department_id": row[5],
        }
        for row in result
    ]
    return {"employees": employees}

# ✅ GET - Retrieve a single employee by ID
@router.get("/api/employees/{employee_id}")
async def get_employee(employee_id: str):
    conn = await get_db_connection()
    async with conn.cursor() as cursor:
        await cursor.execute("SELECT * FROM employee WHERE employee_id = %s", (employee_id,))
        result = await cursor.fetchone()
    
    await conn.ensure_closed()
    
    if result:
        return {
            "employee_id": result[0],
            "employee_name": result[1],
            "gender": result[2],
            "email": result[3],
            "phone": result[4],
            "department_id": result[5],
        }
    raise HTTPException(status_code=404, detail="Employee not found")

# ✅ POST - Add a new employee
@router.post("/api/employees")
async def add_employee(employee: EmployeeCreate):
    try:
        conn = await get_db_connection()
        async with conn.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO employee (employee_id, employee_name, gender, email, phone, department_id) VALUES (%s, %s, %s, %s, %s, %s)",
                (employee.employee_id, employee.employee_name, employee.gender, employee.email, employee.phone, employee.department_id),
            )
            await conn.commit()

        await conn.ensure_closed()
        return {"message": "Employee added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ PUT - Update an employee by ID
@router.put("/api/employees/{employee_id}")
async def update_employee(employee_id: str, employee: EmployeeUpdate):
    try:
        conn = await get_db_connection()
        async with conn.cursor() as cursor:
            await cursor.execute(
                "UPDATE employee SET employee_name=%s, gender=%s, email=%s, phone=%s, department_id=%s WHERE employee_id=%s",
                (employee.employee_name, employee.gender, employee.email, employee.phone, employee.department_id, employee_id),
            )
            await conn.commit()

        await conn.ensure_closed()
        return {"message": "Employee updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ DELETE - Remove an employee by ID
@router.delete("/api/employees/{employee_id}")
async def delete_employee(employee_id: str):
    try:
        conn = await get_db_connection()
        async with conn.cursor() as cursor:
            await cursor.execute("DELETE FROM employee WHERE employee_id = %s", (employee_id,))
            await conn.commit()

        await conn.ensure_closed()
        return {"message": "Employee deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
