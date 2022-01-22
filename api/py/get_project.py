#!/usr/bin/env python3

@app.route('/' + api_path + '/v1/clients/<int:client_id>/projects/<int:project_id>', methods=['GET'])
def get_project(client_id, project_id):

    conn = None

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        cur.execute("""
        SELECT users.id, users.name, users.email
        FROM project_users, users
        WHERE users.id = project_users.user_id AND project_users.project_id = {}
        """.format(project_id))
        ans = cur.fetchall()
        if (len(ans) == 0):
            return jsonify({'code':204})
        ans1 = []
        for row in ans:
            ans1.append(dict(row))
        return jsonify(ans1)
    except (Exception, psycopg2.DatabaseError) as error:
        return str(error)
    finally:
        if conn is not None:
            conn.close()
