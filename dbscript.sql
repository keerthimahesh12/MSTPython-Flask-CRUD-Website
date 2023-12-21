create database tms;
use tms;
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(255),
    email VARCHAR(100)
);
CREATE TABLE tasks (
    task_id INT PRIMARY KEY,
    user_id INT,
    title VARCHAR(100),
    description TEXT,
    category TEXT,
    due_date DATE,
    status BOOLEAN,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);