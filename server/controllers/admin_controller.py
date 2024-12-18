from flask import Blueprint, jsonify, request
from server.services.auth_services import Security
from server.services.admin_services import (get_user_plan, user_query_all_users, is_user_in_db_by_user_id, delete_user_by_user_id, delete_empty_users,
                                get_admin_status_by_id, update_admin_rights_with_id, get_username_by_id)
from server.view.view import invalid_token
from server.utils.settings import SUPER_ADMIN_USERNAME

admin_panel = Blueprint('admin_panel', __name__)

@admin_panel.route('/admin-action/user-list')
def bring_users_list():

    user_data = Security.verify_token(request.headers)
    # If the token is invalid (user_data is False), return 401 Unauthorized
    if not user_data:
        return invalid_token()
    
    users_list = user_query_all_users()

    if users_list:
        return jsonify ({ 'users_list': users_list, 'message': 'User list successfully fetched.'}), 200
    else:
        return jsonify ({"message": "Unable to fetch userlist."}), 400

@admin_panel.route('/admin-action/delete-user/<int:user_id>', methods=['POST'])
def delete_user_from_db(user_id):

    user_data = Security.verify_token(request.headers)
    # If the token is invalid (user_data is False), return 401 Unauthorized
    if not user_data:
        return invalid_token()
    
    username = get_username_by_id(user_id)
    
    if  username == SUPER_ADMIN_USERNAME:
        return jsonify({"message": "Cannot delete SUPER ADMIN."}), 401

    if is_user_in_db_by_user_id(user_id):

        data = request.json
        validation = data.get('validation')

        if validation:
            delete_user_by_user_id(user_id)
            return jsonify({"message": f"User {user_id} deleted."}), 200
        else:
            return delete_empty_users(user_id)
        # send an email to the user that has been deleted. Which can receive more info like /id/int:motive_id
    else:
        return jsonify({"error": "Could find user to delete."}), 401

@admin_panel.route('/admin-action/update-admin-rights/<int:user_id>', methods=["POST"])
def update_admin_rights(user_id):

    username = get_username_by_id(user_id)
    if username == 'admin':
        return jsonify({"message": "Cannot update admin status of SUPER ADMIN."}), 401

    user_data = Security.verify_token(request.headers)
    # If the token is invalid (user_data is False), return 401 Unauthorized
    if not user_data:
        return invalid_token()
        
    if is_user_in_db_by_user_id(user_id):

        admin_status = get_admin_status_by_id(user_id)
        admin_status_msg = "admin." if not admin_status else "commoner."

        update_admin_rights_with_id(user_id, admin_status)
        # send an email to the user that has been updated. Which can receive more info like /id/int:motive_id
        return jsonify({"message": f"User id : {user_id} admin status to updated to {admin_status_msg}", "adminStatus": admin_status})
    
    return jsonify({"message": "Could not update admin status."}), 400

@admin_panel.route('/admin-action/change-plan/<int:user_id>/<int:new_plan>', methods=['POST'])
def update_user_plan(user_id, new_plan):
    user_data = Security.verify_token(request.headers)

    if not user_data:
        return invalid_token()
    try:
        get_user_plan(user_id, new_plan)
        update_plan_msg = "free" if (new_plan == 1) else ("premium" if new_plan == 2 else "premium+")
            
        return jsonify({ "message": f'User id {user_id} plan updated plan to {update_plan_msg} user.'}), 200
    except:
        return jsonify({ "message": f'User plan failed to update.'}),400

## PROVITIONAL ADMIN STATUS REQUEST FOR 1 SINGLE USER

# @admin_panel.route('/admin-action/admin-status/<int:user_id>')
# def get_admin_status(user_id):
#     user_data = Security.verify_token(request.headers)
#     # If the token is invalid (user_data is False), return 401 Unauthorized
#     if not user_data:
#         return invalid_token()
    
#     admin_status = get_admin_status_by_id(user_id)

#     if admin_status:
#         return jsonify({ "message": "Admin status retrieved correctly ", "admin_status": admin_status}), 200
#     else:
#         return jsonify({ "message": "Could not retrieve admin status"}), 400