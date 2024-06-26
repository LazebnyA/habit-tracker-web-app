import React, {useState} from 'react';
import styled from "styled-components";
import { Modal } from 'react-responsive-modal';
import {createGoal} from 'components/Goals/GoalsSlice';
import {useDispatch, useSelector} from "react-redux";
import 'react-responsive-modal/styles.css';

const InnerAddGoalButton = styled.div`
    text-transform: uppercase;
    display: flex;
    align-items: center;
    padding: 3px 12px;
    border-radius: 2px;
    background-color: lightblue;
    cursor: pointer;
    transition: background-color 0.3s, color 0.3s;
    b {
        font-size: 25px;
        margin-right: 12px;
    }
    &:hover {
        color: #e3e3e3;
        background-color: cornflowerblue;
    }
`

const ModalContentContainer = styled.form`
    display: flex;
    flex-direction: column;
    width: 375px;
`

const ModalTitle = styled.div`
    font-size: 30px;
    margin-bottom: 20px;
`


const InputSection = styled.div`
    display: flex;
    flex-direction: column;
    margin-bottom: 15px;
    label {
        margin-bottom: 10px;
    }
    input {
        padding: 5px;
        border: 1px solid #e3e3e3;
        &:focus {
            outline: 1px solid cornflowerblue;
            border-radius: 3px;
            border: none;
        }
    }
`;

const ButtonContainer = styled.div`
    display: flex;
    justify-content: flex-start;
    margin-bottom: 15px;
`;

const SubmitButton = styled.button`
    background-color: cornflowerblue;
    border: none;
    border-radius: 2px;
    padding: 8px 10px 8px 10px;
    color: white;
    font-family: inherit;
    font-size: inherit;
    cursor: pointer;
    opacity: ${(props) => (props.disabled ? 0.7 : 1)};
    pointer-events: ${(props) => (props.disabled ? "none" : "auto")};

    :focus {
        outline: none;
        border: none;
    }
`;

const customModalStyles = `
    .custom-modal .react-responsive-modal-closeButton {
        transition: none;
    }
    .custom-modal .react-responsive-modal-closeButton:hover {
        background-color: transparent !important;
    }
`;


const AddGoalButton = () => {
    const userState = useSelector(state => state.user);
    const {loggedInUser} = userState;

     const [showModal, setShowModal] = useState(false);
     const openModal = () => setShowModal(true);
     const closeModal = () => setShowModal(false);

     const [goalName, setGoalName] = useState("")

     const handleGoalChange = (e) => {
        setGoalName(e.target.value);
     }

     const dispatch = useDispatch()
     const handleSubmit = (e) => {
         e.preventDefault();
         const payload = {email: loggedInUser.email, goalName};
         dispatch(createGoal(payload));
     }

     return (
        <>

            <InnerAddGoalButton onClick={openModal}>
                <b>+</b>    add a goal
            </InnerAddGoalButton>
            <Modal
                open={showModal}
                onClose={closeModal}
                center
                classNames={{ modal: 'custom-modal' }}
            >
                <ModalContentContainer>
                    <ModalTitle>Create a New Goal</ModalTitle>
                    <InputSection>
                        <label htmlFor="createGoal">Enter a Goal Name</label>
                        <input type={"text"} id={"createGoal"} placeholder={"Goal Name"}
                               onChange={handleGoalChange} maxLength={50}/>
                    </InputSection>
                    <ButtonContainer>
                        <SubmitButton type={"submit"} onClick={handleSubmit} disabled={goalName.length === 0}>
                            Add Goal
                        </SubmitButton>
                    </ButtonContainer>
                </ModalContentContainer>
            </Modal>

        </>
    )
}

export default AddGoalButton;