import { useState, useEffect, useCallback } from "react";
import { OnUserAdminAction } from "./adminActions";

export const fetchUsers = async (setUsersList) => {
    try {
        // request for a user list
        const apiBaseUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';
        const url = `${apiBaseUrl}/admin-action/user-list`
        const token = localStorage.getItem('token')
        const options = {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            credentials: 'include'
        }
        const response = await fetch(url, options)
    
        if (response.ok) {
            console.log('Users received.')
            const usersData = await response.json()
            setUsersList(usersData.users_list)
        }
    
        
    } catch (error) {
        console.log(error)
    }
} 

export const AdminPanel = () => {

    const [ usersList, setUsersList ] = useState([]);
    const { handleAdminRights, handleUserDelete } = OnUserAdminAction();

    useEffect(() => {
    
        fetchUsers(setUsersList);
    }, [])

    
    return (

        <div className='admin-panel'>

            {usersList.map((user, key) => {

                    return (
                        <div key={key} className='admin-panel-item'>
                            <span id='user'>{user.username}</span>
                            <span>Created</span>

                            <div className='admin-panel-btn-container'>
                                <div>
                                    <button onClick={ () => handleUserDelete(user.id)} id="admin-delete-btn" className="admin-btn" style={{color: 'white'}} title="delete">
                                        X
                                    </button>

                                </div>
                                <div>
                                    <button onClick={ () => {}} id="admin-change-plan-btn" className="admin-btn" style={{color: 'white'}} title="change-plan">
                                        o
                                    </button>   

                                </div>
                                <div>
                                    <button onClick={ () => handleAdminRights(user.id)} id="admin-admin-rights-btn" className="admin-btn" style={{color: 'white'}} title="admin-rights">
                                        I
                                    </button>   

                                </div>
                            </div>
                                

                        </div>
                        
                    )
                })
            }
                

            </div>

    )

}