import { useState, useEffect, useCallback } from "react";
import { OnUserAdminAction } from "./adminActions";
import { PlanModal } from "./PlanModal"

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
            const usersData = await response.json()
            setUsersList(usersData.users_list)
        }
        
    } catch (error) {
        console.log(error)
    }
} 

export const AdminPanel = ({setHomePageAdminStatus}) => {

    const [ usersList, setUsersList ] = useState([]);
    const [ adminStatus, setAdminStatus] = useState(null);
    const [processingAction, setProcessingAction] = useState(false);
    const [isModalOpen, setModalOpen] = useState(false);
    const [currentUser, setCurrentUser] = useState(null); // modal information


    const { handleAdminRights, handleUserDelete, handleChangePlan } = OnUserAdminAction(() => fetchUsers(setUsersList), setAdminStatus);

    useEffect(() => {
        fetchUsers(setUsersList);
        
    }, [fetchUsers]);

    const adminRightsStyle = (status) => {
        return {
            color: 'white',
            backgroundColor: status ? 'red' : "green",
        };
    }

    const handleOpenModal = (user) => {
        setCurrentUser(user);
        setModalOpen(true);
    };

    const handleCloseModal = () => {
        setModalOpen(false);
        setCurrentUser(null);
    };

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
                                    <button onClick={ () => handleOpenModal(user)} id="admin-change-plan-btn" className="admin-btn" style={{color: 'white'}} title="change-plan">
                                        o
                                    </button>   

                                </div>
                                <div>
                                    <button onClick={ 
                                        async () => {await handleAdminRights(user.id, setProcessingAction, setHomePageAdminStatus);
                                        }} id="admin-admin-rights-btn" className="admin-btn" style={user.adminStatus ? adminRightsStyle(user.adminStatus) :null} title="admin-rights" disabled={processingAction}>
                                        I
                                    </button>   

                                </div>
                            </div>
                                

                        </div>
                        
                    )
                })
            }

            {isModalOpen && (
                        <PlanModal 
                            isOpen={isModalOpen}
                            currentPlan={currentUser?.user_plan}
                            onClose={handleCloseModal}
                            onPlanChange={(newPlan) => handleChangePlan(currentUser.id, newPlan, handleCloseModal)}
                        />
                    )}
                

            </div>

    )

}