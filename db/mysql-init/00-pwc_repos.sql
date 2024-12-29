CREATE DATABASE IF NOT EXISTS grim_db;
USE grim_db;

/* Example DDL */
CREATE TABLE Employees (
    EmployeeID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    BirthDate DATE,
    HireDate DATE,
    Email VARCHAR(100) UNIQUE,
    Salary DECIMAL(10, 2) CHECK (Salary >= 0),
    DepartmentID INT
);
