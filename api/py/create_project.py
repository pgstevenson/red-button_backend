#!/usr/bin/env python3

@app.route('/api/v1/clients/<int:client_id>/projects/create', methods=['GET', 'POST'])
def create_project(client_id):

    conn = None
    if request.args.get('name') is None:
        return jsonify({'code':400, 'key':'name', 'value':'missing'})
    
    parent_id = 'NULL'
    if not request.args.get('parent_id') is None:
        parent_id = request.args['parent_id']

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        cur.execute("""
        INSERT INTO projects (name, parent_id) VALUES ({}, {}) RETURNING id
        """.format(request.args['name'], parent_id))
        project_id = cur.fetchone()[0]
        res = {'code':201, 'project_id':project_id}
        if request.args.get('parent_id') is None:
            cur.execute("""
            INSERT INTO project_users (user_id, project_id, project_admin) VALUES ({}, {}, TRUE) RETURNING id
            """.format(client_id, project_id))
            res['project_users_id'] = cur.fetchone()[0]
        conn.commit()
        return jsonify([res])
    except (Exception, psycopg2.DatabaseError) as error:
        return str(error)
    finally:
        if conn is not None:
            conn.close()
