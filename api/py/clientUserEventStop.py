#!/usr/bin/env python3

@app.route('/' + api_path + '/v1/clients/<int:client_id>/users/<int:user_id>/events/<int:event_id>/stop', methods=['GET', 'PATCH'])
def clientUserEventStop(client_id, user_id, event_id):

    conn = None

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        cur.execute("""UPDATE events SET end_time = CURRENT_TIMESTAMP(0) WHERE id = {}""".format(event_id))
        conn.commit()
        return jsonify([{'code':201}])
    except (Exception, psycopg2.DatabaseError) as error:
        return str(error)
    finally:
        if conn is not None:
            conn.close()
