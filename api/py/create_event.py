#!/usr/bin/env python3

@app.route('/' + api_path + '/v1/clients/<int:client_id>/users/<int:user_id>/events/create', methods=['GET', 'POST'])
def create_event(client_id, user_id):

    conn = None

    if request.args.get('task_id') is None:
        return jsonify({'code':400, 'key':'task_id', 'value':'missing'})

    d = {'user_id': str(user_id),
         'task_id':request.args['task_id'],
         'description': 'NULL'}

    if not request.args.get('description') is None:
        d['description'] = "'" + re.sub("'", "''", request.args['description']) + "'"

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        cur.execute("""INSERT INTO events ({}) VALUES ({}) RETURNING id""".format(",".join(d.keys()), ",".join(d.values())))
        conn.commit()
        return jsonify([{'code':201, 'event_id':cur.fetchone()[0]}])
    except (Exception, psycopg2.DatabaseError) as error:
        return str(error)
    finally:
        if conn is not None:
            conn.close()
