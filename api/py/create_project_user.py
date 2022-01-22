#!/usr/bin/env python3

@app.route('/' + api_path + '/v1/clients/<int:client_id>/projects/<int:project_id>/users/<int:user_id>/create', methods=['GET', 'POST'])
def create_project_user(client_id, project_id, user_id):

    conn = None

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        cur.execute("""
        INSERT INTO project_users (project_id, user_id) VALUES ({}, {}) RETURNING id;
        """.format(project_id, user_id))
        conn.commit()
        return jsonify([{'code':201, 'id':cur.fetchone()[0]}])
    except (Exception, psycopg2.DatabaseError) as error:
        return str(error)
    finally:
        if conn is not None:
            conn.close()
