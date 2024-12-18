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


    const { handleAdminRights, handleUserDelete, handleChangePlan, planModalLoading } = OnUserAdminAction(() => fetchUsers(setUsersList), setAdminStatus);

    useEffect(() => {
        fetchUsers(setUsersList);
        
    }, [fetchUsers]);

    const adminRightsStyle = (status) => {
        return {
            color: 'white',
            backgroundColor: status ? 'rgb(8, 9, 26)' : "green",
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
                                    <button onClick={ () => handleUserDelete(user.id)} id="admin-delete-btn" className="admin-btn" style={{color: 'white'}} title="Delete user">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-trash3" viewBox="0 0 16 16">
                                            <path d="M6.5 1h3a.5.5 0 0 1 .5.5v1H6v-1a.5.5 0 0 1 .5-.5M11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3A1.5 1.5 0 0 0 5 1.5v1H1.5a.5.5 0 0 0 0 1h.538l.853 10.66A2 2 0 0 0 4.885 16h6.23a2 2 0 0 0 1.994-1.84l.853-10.66h.538a.5.5 0 0 0 0-1zm1.958 1-.846 10.58a1 1 0 0 1-.997.92h-6.23a1 1 0 0 1-.997-.92L3.042 3.5zm-7.487 1a.5.5 0 0 1 .528.47l.5 8.5a.5.5 0 0 1-.998.06L5 5.03a.5.5 0 0 1 .47-.53Zm5.058 0a.5.5 0 0 1 .47.53l-.5 8.5a.5.5 0 1 1-.998-.06l.5-8.5a.5.5 0 0 1 .528-.47M8 4.5a.5.5 0 0 1 .5.5v8.5a.5.5 0 0 1-1 0V5a.5.5 0 0 1 .5-.5"/>
                                        </svg>
                                    </button>

                                </div>
                                <div>
                                    <button onClick={ () => handleOpenModal(user)} id="admin-change-plan-btn" className="admin-btn" style={{color: 'white'}} title="Change user plan">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-currency-dollar" viewBox="0 0 16 16">
                                            <path d="M4 10.781c.148 1.667 1.513 2.85 3.591 3.003V15h1.043v-1.216c2.27-.179 3.678-1.438 3.678-3.3 0-1.59-.947-2.51-2.956-3.028l-.722-.187V3.467c1.122.11 1.879.714 2.07 1.616h1.47c-.166-1.6-1.54-2.748-3.54-2.875V1H7.591v1.233c-1.939.23-3.27 1.472-3.27 3.156 0 1.454.966 2.483 2.661 2.917l.61.162v4.031c-1.149-.17-1.94-.8-2.131-1.718zm3.391-3.836c-1.043-.263-1.6-.825-1.6-1.616 0-.944.704-1.641 1.8-1.828v3.495l-.2-.05zm1.591 1.872c1.287.323 1.852.859 1.852 1.769 0 1.097-.826 1.828-2.2 1.939V8.73z"/>
                                        </svg>
                                    </button>   

                                </div>
                                <div>
                                    <button onClick={ 
                                        async () => {await handleAdminRights(user.id, setProcessingAction, setHomePageAdminStatus);
                                        }} id="admin-admin-rights-btn" className="admin-btn" style={user.adminStatus ? adminRightsStyle(user.adminStatus) :null} title="Change admin rights" disabled={processingAction}>
                                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-person-fill-gear" viewBox="0 0 16 16">
                                                <path d="M11 5a3 3 0 1 1-6 0 3 3 0 0 1 6 0m-9 8c0 1 1 1 1 1h5.256A4.5 4.5 0 0 1 8 12.5a4.5 4.5 0 0 1 1.544-3.393Q8.844 9.002 8 9c-5 0-6 3-6 4m9.886-3.54c.18-.613 1.048-.613 1.229 0l.043.148a.64.64 0 0 0 .921.382l.136-.074c.561-.306 1.175.308.87.869l-.075.136a.64.64 0 0 0 .382.92l.149.045c.612.18.612 1.048 0 1.229l-.15.043a.64.64 0 0 0-.38.921l.074.136c.305.561-.309 1.175-.87.87l-.136-.075a.64.64 0 0 0-.92.382l-.045.149c-.18.612-1.048.612-1.229 0l-.043-.15a.64.64 0 0 0-.921-.38l-.136.074c-.561.305-1.175-.309-.87-.87l.075-.136a.64.64 0 0 0-.382-.92l-.148-.045c-.613-.18-.613-1.048 0-1.229l.148-.043a.64.64 0 0 0 .382-.921l-.074-.136c-.306-.561.308-1.175.869-.87l.136.075a.64.64 0 0 0 .92-.382zM14 12.5a1.5 1.5 0 1 0-3 0 1.5 1.5 0 0 0 3 0"/>
                                            </svg>
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
                            modalLoading={planModalLoading}
                        /> 
                    
            )}

            </div>

    )

}