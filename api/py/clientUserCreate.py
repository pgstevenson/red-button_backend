#!/usr/bin/env python3

@app.route('/' + api_path + '/v1/clients/<int:client_id>/users/create', methods=['GET', 'POST'])
def clientUserCreate(client_id):

  conn = None

  d = {'name': "'" + request.args['name'] + "'",
       'email': "'" + request.args['email'] + "'",
       'manager_id': 'NULL'}

  try:
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    cur.execute("""INSERT INTO users ({}) VALUES ({}) RETURNING id""".format(",".join(d.keys()), ",".join(d.values())))
    user_id = cur.fetchone()[0]
    cur.execute("""INSERT INTO client_users (client_id, user_id) VALUES ({}, {}) RETURNING id""".format(client_id, user_id))
    conn.commit()
    return jsonify([{'code': 201, 'user_id': user_id}])
  except (Exception, psycopg2.DatabaseError) as error:
    return str(error)
  finally:
    if conn is not None:
      conn.close()
