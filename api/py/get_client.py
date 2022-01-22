#!/usr/bin/env python3

@app.route('/api/v1/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):

    conn = None
    projects = []
    users = []
    project_users = []

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        
        cur.execute("""
        SELECT * FROM projects WHERE id = ANY(user_projects({}));
        """.format(client_id))
        ans = cur.fetchall()
        for row in ans:
            projects.append(dict(row))
        
        cur.execute("""
        SELECT id, name, email FROM users WHERE id = ANY(client_users({}));
        """.format(client_id))
        ans = cur.fetchall()
        for row in ans:
            users.append(dict(row))
            
        cur.execute("""
        WITH client_projects AS (SELECT project_id FROM project_users WHERE user_id = {})
        SELECT * FROM project_users
        WHERE project_id IN (SELECT project_id FROM client_projects);
        """.format(client_id))
        ans = cur.fetchall()
        for row in ans:
            project_users.append(dict(row))
            
        res = dict(project_users = project_users,
                   projects = projects,
                   users = users)
        
        return jsonify(res)
    except (Exception, psycopg2.DatabaseError) as error:
        return str(error)
    finally:
        if conn is not None:
            conn.close()
