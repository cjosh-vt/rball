from flask import Flask, request
import common_functions_rball
import traceback
import sys

app = Flask(__name__)

@app.route("/login",methods=['GET'])
def login():
    v_username=request.args.get('username')
    v_password=request.args.get('password')

    print ("v_username = " + str(v_username) + " v_password = " + str(v_password) + " g_cursor = " + str(g_cursor))
    
    v_valid_login = get_authentication(g_cursor, v_username, v_password)
    
    print ("got past")
    
    return v_valid_login

def connect_to_postgres():
    return common_functions_rball.get_pg_connection('rball_app','vMBY8kU3E67Cz2ZC','127.0.0.1','nw_rball_app')

def get_authentication(p_cursor,p_username, p_password):
    v_query = ("select player_id, username, password from rball_app.auth_login where username = " + p_username + " and password = " + p_password)
    try:
       p_cursor.execute(v_query)
       v_auth_info = p_cursor.fetchall()
    except:
       sys.exit("Unable to query database...investigate\n" + traceback.format_exc())

    if length(v_auth_info) > 0:
       return v_auth_info[0]
    else:
       return -1
       

if __name__ == '__main__':
    try:
       global g_cursor
       v_conn=connect_to_postgres()
       g_cursor=v_conn.cursor()
       print ("Global Cursor = " + str(g_cursor))
    except:
       sys.exit ("Whoops...you're still dumb...\n" + traceback.format_exc())

    app.run('0.0.0.0',port=80)
