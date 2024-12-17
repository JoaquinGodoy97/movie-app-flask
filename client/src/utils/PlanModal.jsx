export const PlanModal = ({ isOpen, currentPlan, onClose, onPlanChange }) => {
    return (
        <div className={`modal-overlay ${isOpen ? "show" : ""}`}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
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