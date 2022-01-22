/* create the database */
CREATE DATABASE red_button;

/* Define user permssions */
GRANT ALL PRIVILEGES ON DATABASE red_button TO docker;

\connect red_button;

/* Application schemas */

CREATE SCHEMA app
  CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name text,
    email text,
    manager_id int,
    time_zone text default 'Etc/UTC',
    tier int DEFAULT 0,
    client_admin boolean DEFAULT FALSE,
    sys_admin boolean DEFAULT FALSE,
    active boolean DEFAULT TRUE
  )
  CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name text,
    parent_id int
  )
  CREATE TABLE project_users (
    id SERIAL PRIMARY KEY,
    project_id int NOT NULL,
    user_id int NOT NULL,
    project_admin boolean DEFAULT FALSE
  )
  CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    user_id int NOT NULL,
    start_time timestamp with time zone DEFAULT CURRENT_TIMESTAMP(0),
    end_time timestamp with time zone DEFAULT NULL,
    task_id int NOT NULL,
    description text
  );

ALTER DATABASE red_button SET search_path TO app, public;

SET search_path TO app, public;

/* Import data */

INSERT INTO users (id, name, email, manager_id, time_zone, tier, client_admin, sys_admin)
VALUES (1, 'Paul Stevenson', 'paul@pgstevenson.com', NULL, 'Australia/Perth', 0, 't', 't');

INSERT INTO projects (id, name, parent_id)
VALUES (1, 'NON PROJECT', NULL),
       (2, 'Non Billable (Non project)', 1),
       (3, 'General / Manager Approval', 2),
       (4, 'Training', 2);

INSERT INTO project_users (id, project_id, user_id, project_admin)
VALUES (1, 1, 1, 't');

INSERT INTO events (id, user_id, start_time, end_time, task_id, description)
VALUES (1, 5, '2022-01-25 08:30:00 Australia/Perth', '2022-01-25 08:35:00 Australia/Perth', 3, 'Office admin');

 /* Re-set sequences after data upload */

SELECT setval(pg_get_serial_sequence('users', 'id'), MAX(id)) FROM users;
SELECT setval(pg_get_serial_sequence('projects', 'id'), MAX(id)) FROM projects;
SELECT setval(pg_get_serial_sequence('project_users', 'id'), MAX(id)) FROM project_users;
SELECT setval(pg_get_serial_sequence('events', 'id'), MAX(id)) FROM events;

/* Functions */

/*
task_ancestors
For a given task id, return the associated project/service id.
param task_id project id for a given task (level 3)
return a character array of project name/service name/task name
*/
CREATE OR REPLACE FUNCTION task_ancestors (task_id INT)
RETURNS TEXT[] AS
$BODY$
  WITH RECURSIVE parents AS (
       SELECT id, name, parent_id FROM projects WHERE id = task_id
       UNION SELECT c.id, c.name, c.parent_id FROM projects c
     INNER JOIN parents p ON p.parent_id = c.id
       ) SELECT ARRAY (SELECT name FROM parents ORDER BY id asc);
$BODY$
  LANGUAGE sql;

/*
user_ancestors
For a given user_id, return the full manager/ancestor id path to client_id.
return a integer array of manager_id's
*/
CREATE OR REPLACE FUNCTION user_ancestors (user_id INT)
RETURNS INT[] AS
$BODY$
  WITH RECURSIVE parents AS (
       SELECT id, manager_id FROM users WHERE id = user_id
       UNION SELECT c.id, c.manager_id FROM users c
       INNER JOIN parents p ON p.manager_id = c.id
  ) SELECT ARRAY (SELECT id FROM parents);
$BODY$
  LANGUAGE sql;

/*
project_descendants
For a given project_id, returns an array of project id, service id(s), and
task id(s)
param project_id a given project identifier
return an integer array of project/service/task id(s)
*/
CREATE OR REPLACE FUNCTION project_descendants (project_id INT)
RETURNS INT[] AS
$BODY$
  WITH RECURSIVE children AS (
       SELECT id, name, parent_id FROM projects WHERE id = project_id
       UNION SELECT p.id, p.name, p.parent_id FROM projects p
     INNER JOIN children c ON c.id = p.parent_id
   ) SELECT ARRAY (SELECT id FROM children);
$BODY$
  LANGUAGE sql;

/*
client_users
Returns an array of all user_id's nested under a client_id, could also be used
to find all users who are nested under a manager id.
param x user.id
returns an integer array of user.ids
*/
CREATE OR REPLACE FUNCTION client_users (client_id INT)
RETURNS INT[] AS
$BODY$
  WITH RECURSIVE children AS (
       SELECT id, name, manager_id FROM users WHERE id = client_id
       UNION SELECT p.id, p.name, p.manager_id FROM users p
     INNER JOIN children c ON c.id = p.manager_id
   ) SELECT ARRAY (SELECT id FROM children);
$BODY$
  LANGUAGE sql;

/*
user_projects
Returns an array of all project id's (and associated service/task id(s)) to
which a user/client is assigned
param x user.id
returns an integer array of project.ids
*/
CREATE OR REPLACE FUNCTION user_projects (x INT)
RETURNS INT[] AS
$BODY$
  SELECT ARRAY(
    SELECT unnest(project_descendants(project_id)) "id"
    FROM project_users
    WHERE user_id = x)
  AS o
  ORDER BY o;
$BODY$
  LANGUAGE sql;
