import { useCallback, useState } from "react";
import { useToast } from "./ToastMessage";



export const OnUserAdminAction = (fetchUsers, setAdminStatus) => {

    const { showToast } = useToast();

    const handleUserDelete = useCallback(async (user_id, validation=false) => {

        try {
            const token = localStorage.getItem('token')
            const ApiBaseUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';
            const options = {
                method: "POST",
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                credentials: "include",
                body: JSON.stringify({ validation })
            }
            const response = await fetch(`${ApiBaseUrl}/admin-action/delete-user/${user_id}`, options)
            
            if (response.ok) {

                const data = await response.json();
                
                // in case user has movies saved.
                if (data.message && response.status === 206){ 
                    const userRespose = window.confirm(data.message)

                    if (userRespose) {
                        await handleUserDelete(user_id, true)
                        alert("User deleted.")
                    } else {
                        alert("User will not be deleted.")
                    }
                }

                fetchUsers();

            } else {
                console.log("reponse other than 200..", response.status)
            }
        } catch (err) {
            console.log(err)
            // setUserInDatabase(true)
        } 
        

    }, [fetchUsers]);

    const handleChangePlan = useCallback(async (user_id, new_plan, handleCloseModal) => {

        const token = localStorage.getItem('token')
        const ApiBaseUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';
        const options = {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            credentials: "include",
        }
        const response = await fetch(`${ApiBaseUrl}/admin-action/change-plan/${user_id}/${new_plan}`, options)
        
        if (response.ok) {

            const data = await response.json()
            fetchUsers();
            handleCloseModal();
            showToast(data.message)
        }

    }, []);

    const handleAdminRights = useCallback(async (user_id, setProcessingAction, setHomePageAdminStatus) => {

        setProcessingAction(true)
        try {
            const token = localStorage.getItem('token')
            const ApiBaseUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';
            const options = {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                },
                credentials: "include",
            }

            const currentUserId = localStorage.getItem('currentUserId')

            if (user_id == currentUserId){

                const removeCurrentUserRights = window.confirm('You are about to remove your admin rights. Do you want to proceed?')

                if (removeCurrentUserRights){
                    alert('Your admin privileges will be removed.')
                    localStorage.setItem('adminStatus', 'false')
                    setHomePageAdminStatus(false)

                }  else {
                    setHomePageAdminStatus(true);
                    return;
                }
            }

            const response = await fetch(`${ApiBaseUrl}/admin-action/update-admin-rights/${user_id}`, options)
            
            if (response.ok) {

                const data = await response.json()

                const adminStatus = data.adminStatus
                showToast(data.message)
                setAdminStatus(adminStatus ? true : false) //update just 1 single admin status

                fetchUsers();

            } else {
                // console.log("Could not bring data.", response.status)
            }

        } catch (err) {
            console.log(err)
        } finally {
            setProcessingAction(false)
        }


    }, []);

    return {handleAdminRights, handleUserDelete, handleChangePlan};

}