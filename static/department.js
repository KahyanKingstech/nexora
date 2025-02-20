const departmentApiUrl = "http://127.0.0.1:9000/api/departments";

async function fetchDepartments() {
    try {
        let response = await fetch(departmentApiUrl);
        if (!response.ok) throw new Error(`HTTP Error: ${response.status}`);
        
        let data = await response.json();
        let tableBody = document.getElementById("departmentsTable");
        tableBody.innerHTML = "";

        if (!data.departments || !Array.isArray(data.departments)) {
            console.error("Invalid response format:", data);
            return;
        }

        data.departments.forEach(department => {
            let row = `<tr>
                <td>${department.department_id}</td>
                <td>${department.department_name}</td>
                <td>
                    <button id="editDepartmentButton" onclick="editDepartment('${department.department_id}', '${department.department_name}')"><i class="fas fa-edit"></i>  Edit</button>
                    <button id="deleteDepartmentButton" onclick="deleteDepartment('${department.department_id}')"><i class="fas fa-trash"></i>  Delete</button>
                </td>
            </tr>`;
            tableBody.insertAdjacentHTML("beforeend", row);
        });
    } catch (error) {
        console.error("Error fetching departments:", error);
    }
}

async function addDepartment() {
    let department = {
        department_id: document.getElementById("department_id").value,
        department_name: document.getElementById("department_name").value
    };

    if (!department.department_id || !department.department_name) {
        alert("All fields are required");
        return;
    }

    try {
        let response = await fetch(departmentApiUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(department)
        });

        if (!response.ok) {
            let errorData = await response.json();
            alert(errorData.detail || "Failed to add department");
            return;
        }

        alert("Department added successfully");
        fetchDepartments();
        resetDepartmentForm();
    } catch (error) {
        console.error("Error adding department:", error);
    }
}

async function updateDepartment() {
    let department_id = document.getElementById("department_id").value;

    let updatedDepartment = {
        department_name: document.getElementById("department_name").value  // Removed department_id
    };

    try {
        let response = await fetch(`${departmentApiUrl}/${department_id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(updatedDepartment)
        });

        if (!response.ok) {
            let errorData = await response.json();
            alert(errorData.detail || "Failed to update department");
            return;
        }

        alert("Department updated successfully");
        fetchDepartments();
        resetDepartmentForm();
    } catch (error) {
        console.error("Error updating department:", error);
    }
}

async function deleteDepartment(department_id) {
    if (!confirm("Are you sure you want to delete this department?")) return;

    try {
        let response = await fetch(`${departmentApiUrl}/${department_id}`, { method: "DELETE" });

        if (!response.ok) {
            let errorData = await response.json();
            alert(errorData.detail || "Failed to delete department");
            return;
        }

        alert("Department deleted successfully");
        fetchDepartments();
        resetDepartmentForm();
    } catch (error) {
        console.error("Error deleting department:", error);
    }
}

async function loadDepartments() {
    try {
        const response = await fetch(departmentApiUrl); // Replace with your actual API URL
        const data = await response.json();

        const departmentDropdown = document.getElementById("employee_department_id"); // FIXED ID

        // Clear existing options (except the default "Select Department")
        departmentDropdown.innerHTML = '<option value="">Select Department</option>';

        data.departments.forEach(dept => {
            let option = document.createElement("option");
            option.value = dept.department_id;
            option.textContent = `${dept.department_id} - ${dept.department_name}`;
            departmentDropdown.appendChild(option);
        });
    } catch (error) {
        console.error("Error loading departments:", error);
    }
}

function editDepartment(department_id, department_name) {
    document.getElementById("department_id").value = department_id;
    document.getElementById("department_id").disabled = true;  // Fully disable input
    document.getElementById("department_name").value = department_name;

    // Hide Add button and show Update button
    document.getElementById("addDepartmentButton").style.display = "none";
    document.getElementById("updateDepartmentButton").style.display = "inline-block";
}

function resetDepartmentForm() {
    document.getElementById("department_id").value = "";
    document.getElementById("department_id").disabled = false;
    document.getElementById("department_name").value = "";

    // Restore Add button and hide Update button
    document.getElementById("addDepartmentButton").style.display = "inline-block";
    document.getElementById("updateDepartmentButton").style.display = "none";
}

// Call this function when the page loads
document.addEventListener("DOMContentLoaded", loadDepartments);
document.addEventListener("DOMContentLoaded", fetchDepartments);
