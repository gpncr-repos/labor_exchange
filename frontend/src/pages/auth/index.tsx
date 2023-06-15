import React, {useState} from 'react';
import Login from "../../components/auth/login";
import Register from "../../components/auth/register";
import "./styles.css"
const AuthPage = () => {
    const [currentForm, setCurrentForm] = useState('login')

    const toggleForm = (formName: any) => {
        setCurrentForm(formName);
    }

    return (
        <div className="page auth-page">
            {currentForm === 'login' ? <Login onFormSwitch={toggleForm}/> : <Register onFormSwitch={toggleForm}/>}
        </div>
    );
};

export default AuthPage;