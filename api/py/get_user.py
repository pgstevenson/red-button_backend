#!/usr/bin/env python3

@app.route('/api/v1/clients/<int:client_id>/users/<int:user_id>', methods=['GET'])
def get_user(client_id, user_id):

    conn = None
    events = []
    projects = []
    res_client_id = []
    user = []

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        
        cur.execute("""
        SELECT id, name, email, time_zone FROM users WHERE id={}
        """.format(user_id))
        ans = cur.fetchall()
        for row in ans:
            user.append(dict(row))
            
        cur.execute("""
        SELECT d.id, d.name, d.parent_id, project_users.project_admin FROM
        (
            SELECT *, {} as user_id
            FROM projects
            WHERE id = ANY(user_projects({}))
        ) d
        LEFT JOIN project_users
        ON project_users.project_id = d.id
        AND project_users.user_id = d.user_id;
        """.format(user_id, user_id))
        ans = cur.fetchall()
        for row in ans:
            projects.append(dict(row))
            
        cur.execute("""
        WITH tz AS (SELECT time_zone FROM users WHERE id={} LIMIT 1)
        SELECT id,
            to_char(start_time AT TIME ZONE (SELECT * FROM tz), 'YYYY-MM-DD"T"HH24:MI:SS') AS start_time,
            to_char(end_time AT TIME ZONE (SELECT * FROM tz), 'YYYY-MM-DD"T"HH24:MI:SS') AS end_time,
            task_id,
            description,
            task_ancestors(task_id) AS task
        FROM events
        WHERE user_id={}
        ORDER BY start_time DESC;""".format(user_id, user_id))
        ans = cur.fetchall()
        for row in ans:
            events.append(dict(row))
        
        cur.execute("""
        SELECT id FROM users WHERE id = ANY(user_ancestors({})) AND manager_id IS NULL;
        """.format(user_id))
        res_client_id = cur.fetchone()[0]
        
        res = dict(events = events, projects = projects, user = user)
        res['client_id'] = res_client_id
            
        return jsonify(res)
    except (Exception, psycopg2.DatabaseError) as error:
        return str(error)
    finally:
        if conn is not None:
            conn.close()
