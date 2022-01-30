#!/usr/bin/env python3

@app.route('/' + api_path + '/v1/clients/<int:client_id>/projects', methods=['GET'])
def clientProjectsGet(client_id):
  conn = None
  ans1 = []
  try:
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    cur.execute("""
    SELECT * FROM projects WHERE id = ANY(user_projects({}));
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

# @app.route('/' + api_path + '/v1/clients/<int:client_id>/proejcts/<int:project_id>/users', methods=['GET'])
# def clientProjectUsersGet(client_id):
#   conn = None
#   ans1 = []
#   try:
#     params = config()
#     conn = psycopg2.connect(**params)
#     cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
#     cur.execute("""
#     WITH client_projects AS (SELECT project_id FROM project_users WHERE user_id = {})
#     SELECT * FROM project_users
#     WHERE project_id IN (SELECT project_id FROM client_projects);
#     """.format(client_id))
#     ans = cur.fetchall()
#     if (len(ans) == 0):
#       return jsonify({'code':204})
#     for row in ans:
#       ans1.append(dict(row))
#     return jsonify(ans1)
#   except (Exception, psycopg2.DatabaseError) as error:
#     return str(error)
#   finally:
#     if conn is not None:
#       conn.close()
