#!/usr/bin/env python3

@app.route('/' + api_path + '/v1/clients/<int:client_id>/users/<int:user_id>/projects', methods=['GET'])
def clientUserProjectsGet(client_id, user_id):
  conn = None
  ans1 = []
  try:
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    cur.execute("""
    SELECT d.id, d.name, d.parent_id, project_users.project_admin FROM
    (
      SELECT *, {} as user_id
      FROM projects
      WHERE id = ANY(user_projects({}))
    ) d
    LEFT JOIN project_users
    ON project_users.project_id = d.id
    AND project_users.user_id = d.user_id;
    """.format(user_id, user_id))
    ans = cur.fetchall()
    if (len(ans) == 0):
      return jsonify({'code':204})
    ans1 = []
    for row in ans:
      ans1.append(dict(row))
    return jsonify(ans1)
  except (Exception, psycopg2.DatabaseError) as error:
    return str(error)
  finally:
    if conn is not None:
      conn.close()
