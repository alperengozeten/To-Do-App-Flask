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
       ('Clean the house', 'Clean the whole house', 'Done', '2023-03-18 12:00:00', '2023-03-14 09:00:00', '2023-03-18 17:00:00', 1, 'Lifestyle'),
       ('Submit report', 'Submit quarterly report', 'Todo', '2023-04-12 17:00:00', '2023-03-21 13:00:00', NULL, 1, 'Job'),
       ('Call Mom', 'Call Mom and wish her', 'Todo', '2023-04-06 11:00:00', '2023-03-23 12:00:00', NULL, 1, 'Family'),
       ('Gym workout', 'Do weight training for an hour', 'Done', '2023-03-19 14:00:00', '2023-03-12 10:00:00', '2023-03-19 11:00:00', 1, 'Health'),
       ('Play guitar', 'Learn new song for an hour', 'Todo', '2023-04-05 20:00:00', '2023-03-20 14:00:00', NULL, 2, 'Hobbies'),
       ('Book flights', 'Book flights for summer vacation', 'Done', '2023-03-16 09:00:00', '2023-03-13 13:00:00', '2023-03-16 11:00:00', 2, 'Lifestyle'),
       ('Write a blog post', 'Write about recent project', 'Todo', '2023-04-11 17:00:00', '2023-03-22 09:00:00', NULL, 2, 'Job'),
       ('Grocery shopping', 'Buy groceries for the week', 'Todo', '2023-04-05 18:00:00', '2023-03-31 10:00:00', NULL, 2, 'Family'),
       ('Painting', 'Paint a landscape for 2 hours', 'Done', '2023-03-23 15:00:00', '2023-03-18 14:00:00', '2023-03-23 16:00:00', 2, 'Hobbies');
