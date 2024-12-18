import { LoadingPage } from "./LoadingPage";

export const PlanModal = ({ isOpen, currentPlan, onClose, onPlanChange, modalLoading }) => {

    const loadingOverListStyle = {
        // display: 'flex',
        position: 'absolute',
        // width: '100%',
        // height: '100%',

        top: '15%',
        zIndex: '1001',
    }
    console.log(modalLoading)

    return (


        <div className={`modal-overlay ${isOpen ? "show" : ""}`}>
            {modalLoading && (
                <div className="loading-spinner " style={loadingOverListStyle}>
                    <LoadingPage />
                </div>
                )}

            <div className="modal-content" onClick={(e) => e.stopPropagation()} style={{opacity: modalLoading ? 0.5 : 1}}>
                
                <h3>Select a Plan</h3>
                <div className="plan-buttons">
                    <button 
                        onClick={() => onPlanChange(1)} 
                        disabled={currentPlan === 1}
                    >
                        Free
                    </button>
                    <button 
                        onClick={() => onPlanChange(2)} 
                        disabled={currentPlan === 2}
                    >
                        Premium
                    </button>
                    <button 
                        onClick={() => onPlanChange(3)} 
                        disabled={currentPlan === 3}
                    >
                        Premium Plus
                    </button>
                </div>
                <button className="modal-close-btn" onClick={onClose}>Close</button>
            </div>
        </div>
    );
};