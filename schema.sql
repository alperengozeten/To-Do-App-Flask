CREATE DATABASE IF NOT EXISTS cs353hw4db;
USE cs353hw4db;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS TaskType;
DROP TABLE IF EXISTS Task;
CREATE TABLE User (
    id int NOT NULL AUTO_INCREMENT,
    password varchar(255) NOT NULL,
    username varchar(255) NOT NULL,
    email varchar(255) NOT NULL,
    PRIMARY KEY (id)
);
CREATE TABLE TaskType (
    type varchar(255) NOT NULL,
    PRIMARY KEY (type)
);
CREATE TABLE Task(
    id int NOT NULL AUTO_INCREMENT,
    title varchar(255),
    description text,
    status varchar(255),
    deadline datetime,
    creation_time datetime,
    done_time datetime,
    user_id int,
    task_type varchar(255),
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (task_type) REFERENCES TaskType(type)
);
INSERT INTO User(password, username, email)
VALUES ('pass123', 'user1', 'user1@example.com'),
       ('password', 'user2', 'user2@example.com');
INSERT INTO TaskType
VALUES ('Health'),
       ('Job'),
       ('Lifestyle'),
       ('Family'),
       ('Hobbies');
INSERT INTO Task(title, description, status, deadline, creation_time, done_time, user_id, task_type)
VALUES ('Go for a walk', 'Walk for at least 30 mins', 'Done', '2023-03-20 17:00:00', '2023-03-15 10:00:00', '2023-03-20 10:00:00', 1, 'Health'),
       ('Clean the house', 'Clean the whole house', 'Done', '2023-03-18 12:00:00', '2023-03-14 09:00:00', '2023-03-18 17:00:00', 1, 'Lifestyle');
