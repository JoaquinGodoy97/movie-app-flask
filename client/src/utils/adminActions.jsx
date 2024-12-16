import { useCallback, useState } from "react";
import { fetchUsers } from "./adminPanel";


export const OnUserAdminAction = () => {

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
                console.log(response)   
                const data = await response.json();

                if (data.message && response.status === 206){ 
                    const userRespose = window.confirm(data.message)

                    if (userRespose) {
                        await handleUserDelete(user_id, true)
                        alert("User deleted.")
                    } else {
                        alert("User will not be deleted.")
                    }
                }
                // setUserInDatabase(false)
            } else {
                console.log("reponse other than 200..", response.status)
            }
        } catch (err) {
            console.log(err)
            // setUserInDatabase(true)
        } 
        

    }, [fetchUsers]);

    // const handleChangePlan = useCallback(async () => {

    //     const token = localStorage.getItem('token')
    //     const ApiBaseUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';
    //     const options = {
    //         method: "POST",
    //         headers: {
    //             "Authorization": `Bearer ${token}`
    //         },
    //         credentials: "include",
    //     }
    //     const response = await fetch(`${ApiBaseUrl}/admin-action/delete-user/${user_id}`, options)
        
    //     if (response.ok) {
    //         console.log(response)
    //     }

    // }, []);

    const handleAdminRights = useCallback(async (user_id, admin_status) => {

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
            const response = await fetch(`${ApiBaseUrl}/admin-action/update-admin-rights/${user_id}`, options)
            
            if (response.ok) {
                console.log(response)
            } else {
                console.log("reponse other than 200..", response.status)
            }
        } catch (err) {
            console.log(err)
        }


    }, []);

    return {handleAdminRights, handleUserDelete};

}

    