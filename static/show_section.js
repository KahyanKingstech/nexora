document.addEventListener("DOMContentLoaded", () => {
    showSection('home');
});

function showSection(section) {
    document.getElementById("homeSection").style.display = "none";
    document.getElementById("departmentSection").style.display = "none";
    document.getElementById("employeeSection").style.display = "none";

    if (section === "departments") {
        document.getElementById("departmentSection").style.display = "block";
    } else if (section === "employees") {
        document.getElementById("employeeSection").style.display = "block";
    } else {
        document.getElementById("homeSection").style.display = "block";
    }
}