/*Inserting rows into the 'users' table*/
INSERT INTO users (user_id, username, password, email)
VALUES
  (1, 'user1', 'password1', 'user1@example.com'),
  (2, 'user2', 'password2', 'user2@example.com'),
  (3, 'user3', 'password3', 'user3@example.com'),
  (4, 'user4', 'password4', 'user4@example.com'),
  (5, 'user5', 'password5', 'user5@example.com');

/*Inserting rows into the 'tasks' table*/
INSERT INTO tasks (task_id, user_id, title, description, category, due_date, status)
VALUES
  (1, 1, 'Complete Report', 'Finish the quarterly report for the team', 'Official', '2023-01-15', false),
  (2, 2, 'Prepare Presentation', 'Create a presentation for the upcoming meeting', 'Official', '2023-02-10', true),
  (3, 3, 'Personal Project', 'Work on a personal coding project', 'Unofficial', '2023-03-20', false),
  (4, 4, 'Meeting with Client', 'Discuss project details with a client', 'Official', '2023-04-05', true),
  (5, 5, 'Research New Technologies', 'Explore and research new technologies in the industry', 'Other', '2023-05-30', false);
