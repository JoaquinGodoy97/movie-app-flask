import {Toast} from 'react-bootstrap';
import { useState, useContext, createContext } from 'react';

const ToastContext = createContext();

export const ToastProvider = ({ children }) => {

    const [toastMessage, setToastMessage] = useState(null);

    const showToast = (message) => {
        setToastMessage(message);
        setTimeout(() => setToastMessage(null), 3000); // Clear toast after 3 seconds
    };

    return (
        <ToastContext.Provider value={{ showToast }}>
            {children}
            {toastMessage && (
                <Toast className='toast-message'>
                    <Toast.Body>{toastMessage}</Toast.Body>
                </Toast>
            )}
        </ToastContext.Provider>
    );
};

export const useToast = () => useContext(ToastContext);