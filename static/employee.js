const employeeApiUrl = "http://127.0.0.1:9000/api/employees";

async function fetchEmployees() {
    try {
        let response = await fetch(employeeApiUrl);
        if (!response.ok) throw new Error(`HTTP Error: ${response.status}`);
        
        let data = await response.json();
        let tableBody = document.getElementById("employeesTable");
        tableBody.innerHTML = "";

        if (!data.employees || !Array.isArray(data.employees)) {
            console.error("Invalid response format:", data);
            return;
        }

        data.employees.forEach(employee => {
            let row = `<tr>
                <td>${employee.employee_id}</td>
                <td>${employee.employee_name}</td>
                <td>${employee.gender}</td>
                <td>${employee.email}</td>
                <td>${employee.phone}</td>
                <td>${employee.department_id}</td>
                <td>
                    <button id="editEmployeeButton" onclick="editEmployee('${employee.employee_id}', '${employee.employee_name}', '${employee.gender}', '${employee.email}', '${employee.phone}', '${employee.department_id}')"><i class="fas fa-edit"></i>  Edit</button>
                    <button id="deleteEmployeeButton" onclick="deleteEmployee('${employee.employee_id}')"><i class="fas fa-trash"></i>  Delete</button>
                </td>
            </tr>`;
            tableBody.insertAdjacentHTML("beforeend", row);
        });
    } catch (error) {
        console.error("Error fetching employees:", error);
    }
}

async function addEmployee() {
    let employee = {
        employee_id: document.getElementById("employee_id").value,
        employee_name: document.getElementById("employee_name").value,
        gender: document.getElementById("gender").value,
        email: document.getElementById("email").value,
        phone: document.getElementById("phone").value,
        department_id: document.getElementById("employee_department_id").value // Corrected reference
    };

    if (!employee.employee_id || !employee.employee_name || !employee.gender || 
        !employee.email || !employee.phone || !employee.department_id) {
        alert("All fields are required");
        return;
    }

    try {
        const response = await fetch(employeeApiUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(employee)
        });

        if (!response.ok) {
            const errorData = await response.text();
            throw new Error(`Error: ${response.status} - ${errorData}`);
        }

        alert("Employee added successfully");
        fetchEmployees();
        resetEmployeeForm();
    } catch (error) {
        console.error("Failed to add employee:", error);
    }
}

async function updateEmployee() {
    let employee_id = document.getElementById("employee_id").value;
    let updatedEmployee = {
        employee_name: document.getElementById("employee_name").value,
        gender: document.getElementById("gender").value,
        email: document.getElementById("email").value,
        phone: document.getElementById("phone").value,
        department_id: document.getElementById("employee_department_id").value
    };

    try {
        let response = await fetch(`${employeeApiUrl}/${employee_id}`, { // Ensure API matches expected format
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(updatedEmployee)
        });

        if (!response.ok) {
            let errorData = await response.json();
            alert(errorData.detail || "Failed to update employee");
            return;
        }

        alert("Employee updated successfully");
        fetchEmployees(); 
        resetEmployeeForm();
    } catch (error) {
        console.error("Error updating employee:", error);
    }
}

async function deleteEmployee(employee_id) {
    if (!confirm("Are you sure you want to delete this employee?")) return;

    try {
        let response = await fetch(`${employeeApiUrl}/${employee_id}`, { method: "DELETE" });

        if (!response.ok) {
            let errorData = await response.json();
            alert(errorData.detail || "Failed to delete employee");
            return;
        }

        alert("Employee deleted successfully");
        fetchEmployees();
        resetEmployeeForm();
    } catch (error) {
        console.error("Error deleting employee:", error);
    }
}

function editEmployee(employee_id, employee_name, gender, email, phone, department_id) {
    document.getElementById("employee_id").value = employee_id;
    document.getElementById("employee_id").disabled = true;
    document.getElementById("employee_name").value = employee_name;
    document.getElementById("gender").value = gender;
    document.getElementById("email").value = email;
    document.getElementById("phone").value = phone;
    document.getElementById("employee_department_id").value = department_id;

    document.getElementById("updateEmployeeButton").style.display = "inline-block";
    document.getElementById("addEmployeeButton").style.display = "none";
}

function resetEmployeeForm() {
    document.getElementById("employee_id").value = "";
    document.getElementById("employee_id").disabled = false;
    document.getElementById("employee_name").value = "";
    document.getElementById("gender").value = "";
    document.getElementById("email").value = "";
    document.getElementById("phone").value = "";
    document.getElementById("employee_department_id").value = "";

    document.getElementById("updateEmployeeButton").style.display = "none";
    document.getElementById("addEmployeeButton").style.display = "inline-block";
}

document.addEventListener("DOMContentLoaded", fetchEmployees);
