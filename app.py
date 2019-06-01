from flask import Flask, request, jsonify
import common_functions_rball
import traceback
import sys

app = Flask(__name__)

@app.route("/login",methods=['GET'])
def login():
    v_username=request.args.get('username')
    v_password=request.args.get('password')

    v_player_id = get_authentication(g_cursor, v_username, v_password)
    
    if v_player_id == -1:
        return jsonify(player_id="PLAYER NOT FOUND")
    else:
        return jsonify(player_id=v_player_id)
        
@app.route("/playerInfo",methods=['GET'])
def playerInfo():
    v_player_id=request.args.get('playerID')

    v_player_info = get_player_info(g_cursor, v_player_id)
    
    print (v_player_info)
    
    return v_player_info
        


def connect_to_postgres():
    return common_functions_rball.get_pg_connection('rball_app','vMBY8kU3E67Cz2ZC','127.0.0.1','nw_rball_app')

def get_player_info(p_cursor,p_player_id):
    v_query = ("select player_first_name, player_last_name, player_phone, player_email, season_description, skill_description, is_administrator from rball_app.player_info where player_id = " + str(p_player_id))
    print (v_query)
    try:
       print ("trying to run the query...again")
       p_cursor.execute(v_query)
       v_player_info = p_cursor.fetchall()
       print (v_player_info)
    except:
       print ("Unable to query player information...investigate\n" + traceback.format_exc())
    else:
       return jsonify(player_first_name=v_player_info[0][0],
          player_last_name=v_player_info[0][1],
          player_phone=v_player_info[0][2],
          player_email=v_player_info[0][3],
          season_description=v_player_info[0][4],
          skill_description=v_player_info[0][5],
          is_administrator=v_player_info[0][6])

def get_authentication(p_cursor,p_username, p_password):
    v_query = ("select player_id from rball_app.auth_login where username = '" + p_username + "' and password = '" + p_password + "'")
    try:
       p_cursor.execute(v_query)
       v_auth_info = p_cursor.fetchall()
    except:
       print("Unable to query database...investigate\n" + traceback.format_exc())

    if len(v_auth_info) > 0:
       return v_auth_info[0][0]
    else:
       return -1

def get_connection():
    try:
       global g_cursor
       v_conn=connect_to_postgres()
       g_cursor=v_conn.cursor()
    except:
       print ("Whoops...you're still dumb...\n" + traceback.format_exc())
       

if __name__ == '__main__':

    get_connection()
    
    app.run('0.0.0.0',port=80)
