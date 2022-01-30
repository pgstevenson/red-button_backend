#!/usr/bin/env python3

@app.route('/' + api_path + '/v1/clients/<int:client_id>/users/<int:user_id>/events/<int:event_id>', methods=['GET'])
def clientUserEventGet(client_id, user_id, event_id):
  conn = None
  ans1 = []
  try:
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    cur.execute("""
    WITH tz AS (SELECT time_zone FROM users WHERE id={} LIMIT 1)
    SELECT id,
      to_char(start_time AT TIME ZONE (SELECT * FROM tz), 'YYYY-MM-DD"T"HH24:MI:SS') AS start_time,
      to_char(end_time AT TIME ZONE (SELECT * FROM tz), 'YYYY-MM-DD"T"HH24:MI:SS') AS end_time,
      task_id,
      description,
      task_ancestors(task_id) AS task
    FROM events
    WHERE user_id={}
    ORDER BY start_time DESC
    LIMIT 1 OFFSET {};""".format(user_id, user_id, event_id))
    ans = cur.fetchall()
    if (len(ans) == 0):
      return jsonify({'code':204})
    for row in ans:
      ans1.append(dict(row))
    return jsonify(ans1[0])
  except (Exception, psycopg2.DatabaseError) as error:
    return str(error)
  finally:
    if conn is not None:
      conn.close()
