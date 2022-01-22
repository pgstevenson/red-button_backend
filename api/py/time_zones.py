#!/usr/bin/env python3

@app.route('/' + api_path + '/v1/time_zones', methods=['GET'])
def time_zones():

  conn = None
  res = []

  try:
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    cur.execute("""SELECT name, abbrev, is_dst FROM pg_timezone_names;""")
    ans = cur.fetchall()
    if (len(ans) == 0):
        return jsonify({'code':204})
    for row in ans:
        res.append(dict(row))
    return jsonify(res)
  except (Exception, psycopg2.DatabaseError) as error:
    return str(error)
  finally:
    if conn is not None:
      conn.close()
