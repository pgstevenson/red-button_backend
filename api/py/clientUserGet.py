#!/usr/bin/env python3

@app.route('/' + api_path + '/v1/clients/<int:client_id>/users/<int:user_id>', methods=['GET'])
def clientUserGet(client_id, user_id):
  conn = None
  ans1 = []
  try:
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    cur.execute("""
    SELECT id, name, email, time_zone FROM users WHERE id={} LIMIT 1
    """.format(user_id))
    ans = cur.fetchall()
    if (len(ans) == 0):
      return jsonify({'code':204})
    for row in ans:
      ans1.append(dict(row))
    cur.execute("""
    SELECT id FROM users WHERE id = ANY(user_ancestors({})) AND manager_id IS NULL LIMIT 1;
    """.format(user_id))
    # ans1 = cur.fetchone()[0]
    ans1[0]['client_id'] = cur.fetchone()[0]
    return jsonify(ans1)
  except (Exception, psycopg2.DatabaseError) as error:
    return str(error)
  finally:
    if conn is not None:
      conn.close()
