from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import get_db_connection

router = APIRouter()

# Define request model
class Department(BaseModel):
    department_id: str
    department_name: str

# ✅ GET - Retrieve all departments
@router.get("/api/departments")
async def get_departments():
    conn = await get_db_connection()  # ✅ Await the connection
    async with conn.cursor() as cursor:
        await cursor.execute("SELECT department_id, department_name FROM department")
        result = await cursor.fetchall()
    
    conn.close()
    
    # Convert to JSON format
    departments = [{"department_id": row[0], "department_name": row[1]} for row in result]
    return {"departments": departments}



# ✅ POST - Add a new department
@router.post("/api/departments")
async def add_department(department: Department):
    try:
        conn = await get_db_connection()  # ✅ Await the async function
        async with conn.cursor() as cursor:
            await cursor.execute("INSERT INTO department (department_id, department_name) VALUES (%s, %s)",
                               (department.department_id, department.department_name))
            await conn.commit()

        await conn.ensure_closed()
        return {"message": "Department added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ PUT - Update an existing department
@router.put("/api/departments/{department_id}")
async def update_department(department_id: str, updated_department: Department):
    try:
        conn = await get_db_connection()
        async with conn.cursor() as cursor:
            await cursor.execute("UPDATE department SET department_name = %s WHERE department_id = %s",
                               (updated_department.department_name, department_id))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Department not found")
            await conn.commit()
        
        await conn.ensure_closed()
        return {"message": "Department updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ DELETE - Remove a department
@router.delete("/api/departments/{department_id}")
async def delete_department(department_id: str):
    try:
        conn = await get_db_connection()
        async with conn.cursor() as cursor:
            await cursor.execute("DELETE FROM department WHERE department_id = %s", (department_id,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Department not found")
            await conn.commit()
        
        await conn.ensure_closed()
        return {"message": "Department deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
