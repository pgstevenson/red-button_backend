#!/usr/bin/env python3

@app.route('/' + api_path + '/v1/clients/<int:client_id>/users/<int:user_id>/events/<int:event_id>/update', methods=['GET', 'PATCH'])
def update_event(client_id, user_id, event_id):

    conn = None

    if len(request.args) == 0:
        return jsonify({'code':422, 'value':'Nothing to change'})

    d = []

    if not request.args.get("start_time") is None:
        d.append("start_time = '" + request.args["start_time"].replace("T", " ", 1) + "'")
    if not request.args.get("end_time") is None:
        d.append("end_time = '" + request.args["end_time"].replace("T", " ", 1) + "'")
    if not request.args.get("task_id") is None:
        d.append("task_id = " + request.args["task_id"])
    if not request.args.get("description") is None:
        d.append("description = '" + re.sub("'", "''", request.args['description']) + "'")

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        cur.execute("""UPDATE events SET {} WHERE id = {};""".format(', '.join(d), event_id))
        conn.commit()
        return jsonify([{'code':200}])
    except (Exception, psycopg2.DatabaseError) as error:
        return str(error)
    finally:
        if conn is not None:
            conn.close()
