import { useState, useEffect } from "react";

export const AdminPanel = () => {

    const [ usersList, setUsersList ] = useState([])

    useEffect(() => {

        const fetchUsers = async () => {
            try {
                // request for a user list
                const apiBaseUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';
                const url = `${apiBaseUrl}/user-list`
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
        
        //     console.log("Showing list of users: ", usersData)
        // } catch (err) {
        //     console.log("Could not fetch users list.")
        // }

        // setUsersList([{id: 1, username: 'pedro'},{id: 2, username: 'juan'},{id: 3, username: 'raul'} ])

        fetchUsers();

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
                                    <button id="admin-delete-btn" className="admin-btn" style={{color: 'white'}} title="delete">
                                        X
                                    </button>

                                </div>
                                <div>
                                    <button id="admin-change-plan-btn" className="admin-btn" style={{color: 'white'}} title="change-plan">
                                        o
                                    </button>   

                                </div>
                                <div>
                                    <button id="admin-admin-rights-btn" className="admin-btn" style={{color: 'white'}} title="admin-rights">
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