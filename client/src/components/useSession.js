import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { checkSession } from './utils/check_session';

export function useSession() {
    const [sessionChecked, setSessionChecked] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        async function verifySession() {
            try {
                const sessionStatus = await checkSession();
                if (!sessionStatus.logged_in) {
                    navigate('/login');
                }
                setSessionChecked(true); // Session check is complete
            } catch (error) {
                console.error('Error checking session:', error);
                navigate('/login');
            }
        }

        verifySession();
    }, [navigate]);

    return sessionChecked;
}