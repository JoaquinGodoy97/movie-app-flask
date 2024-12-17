from flask import jsonify
from server.utils.db_connection import get_db_connection
from server.models.user_model import User
from mysql import connector

def update_super_admin_rights(username):

    update_query = """
        UPDATE users 
        SET is_admin = TRUE 
        WHERE username = %s;
        """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(update_query, (username,))
        connection.commit()
        print("Admin privileges updated successfuly.")
    except:
        print("Could not add super admin privileges.")
    finally:
        cursor.close()
        connection.close()

def user_query_all_users():
    query = "SELECT * FROM users;"

    users_list = []

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        found_users = cursor.fetchall()

        for user in found_users:
            instanced_user = User(user[0], user[1], user[2], user[3], user[4], user[5])  # ID, User, Email, Pass, admin rights

            users_list.append({
                "id": instanced_user.id,
                "username": instanced_user.username,
                "email": instanced_user.email,
                "password": instanced_user.password,
                "adminStatus": instanced_user.admin_status,
                "user_plan": instanced_user.user_plan

            })
        
        return users_list
    
    except:
        print("Coul not bring list of users")
        return None
    finally:
        cursor.close()
        connection.close()

def delete_user_by_user_id(user_id):

    username = get_username_by_id(user_id)

    if not username: 
        print(f"User with ID {user_id} not found.") 
        return

    query = """
        DELETE FROM wishlist_user
        WHERE username = %s"""

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(query, (username,))
        connection.commit()
        print(f"Movies from {user_id} were deleted correctly.")
    except Exception as e:
        print("Failed to delete user:", e)
        return None
    finally:
        cursor.close()
        connection.close()
    
    return delete_empty_users(user_id)

def delete_empty_users(user_id):
    query = """
            DELETE FROM users
            WHERE id = %s"""
        
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(query, (user_id,))
        connection.commit()
        print(f"User id {user_id} deleted correctly.")

        return jsonify({"message": f"User {user_id} deleted."}), 200
    except:
        print("Failed to delete user")
        return jsonify({ "message": f"The user {user_id} have movies saved. Would you like to delete it anyways?"}), 206
        
    finally:
        cursor.close()
        connection.close()

def is_user_in_db_by_user_id(user_id):
    query = "SELECT * FROM users WHERE id = %s"

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(query, (user_id,))
        found_user = cursor.fetchone()

        if found_user:
            return True
        else:
            return False
        
    except connector.Error as e:
        print(f"Could not find user: {e}")
    finally:
        cursor.close()
        connection.close()

def update_admin_rights_with_id(user_id, admin_status):
        update_admin_status = 0 if admin_status else 1

        update_query = """
        UPDATE users 
        SET is_admin =  %s
        WHERE id = %s;
        """

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(update_query, (update_admin_status, user_id,))
            connection.commit()

        except Exception as e:
            print("Coul not update admin status.:", e)
        finally:
            cursor.close()
            connection.close()


def get_admin_status_by_id(user_id):
    query = "SELECT is_admin FROM users WHERE id = %s;"

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(query, (user_id,))
        admin_status = cursor.fetchone()[0]

        return admin_status
    
    except:
        print("Coul not bring admin status.")
        return None
    finally:
        cursor.close()
        connection.close()

def get_username_by_id(user_id):
    query = "SELECT username FROM users WHERE id = %s;"

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(query, (user_id,))
        username = cursor.fetchone()[0]
        return username
    
    except:
        print("Coul not bring username.")
        return None
    finally:
        cursor.close()
        connection.close()

def get_user_plan(user_id, update_plan):
    query = "UPDATE users SET user_plan = %s WHERE id = %s;"

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(query, (update_plan, user_id))
        connection.commit()

    except:
        print("Coul not bring username.")
        return None
    finally:
        cursor.close()
        connection.close()



# def get_all_admin_rights():
#     query = "SELECT admin_status FROM users;"

#     try:
#         connection = get_db_connection()
#         cursor = connection.cursor()
#         cursor.execute(query)
#         admin_status = cursor.fetchone()[0]

#         return admin_status
    
#     except:
#         print("Coul not bring admin status.")
#         return None
#     finally:
#         cursor.close()
#         connection.close()
