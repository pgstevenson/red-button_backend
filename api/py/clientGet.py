#!/usr/bin/env python3

@app.route('/' + api_path + '/v1/clients/<int:client_id>', methods=['GET'])
def clientGet(client_id):
  conn = None
  ans1 = []
  try:
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    cur.execute("""
    SELECT id, name, email FROM users WHERE id = ANY(client_users({}));
    """.format(client_id))
    ans = cur.fetchall()
    if (len(ans) == 0):
      return jsonify({'code':204})
    for row in ans:
      ans1.append(dict(row))
    return jsonify(ans1)
  except (Exception, psycopg2.DatabaseError) as error:
    return str(error)
  finally:
    if conn is not None:
      conn.close()
