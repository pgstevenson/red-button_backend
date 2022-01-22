#!/usr/bin/env python3

@app.route('/api/v1/clients/create', methods=['GET', 'POST'])
def create_client():
  
  conn = None
  
  if request.args.get('name') is None:
    return jsonify({'code':400, 'key':'name'})
  if request.args.get('email') is None:
    return jsonify({'code':400, 'key':'email'})

  d = {'name': "'" + request.args['name'] + "'",
       'email': "'" + request.args['email'] + "'",
       'time_zone': "'" + request.args['time_zone'] + "'",
       'tier': request.args['tier'],
       'manager_id': 'NULL',
       'client_admin': 'TRUE',
       'active': 'FALSE'}
       
  try:
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    cur.execute("""INSERT INTO users ({}) VALUES ({}) RETURNING id""".format(",".join(d.keys()), ",".join(d.values())))
    res = cur.fetchone()[0]
    conn.commit()
    return jsonify([{'code': 201, 'id': res}])
  except (Exception, psycopg2.DatabaseError) as error:
    return str(error)
  finally:
    if conn is not None:
      conn.close()
