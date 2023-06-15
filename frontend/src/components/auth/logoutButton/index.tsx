import React from 'react';
import useAuth from "../../../hooks/useAuth";
import './styles.css'

const LogoutButton = () => {
    const { setAuth } = useAuth()

    const logout = async () => {
        setAuth({});
        localStorage.setItem('auth', JSON.stringify({}));
    }

    return (
        <button onClick={logout} className="logout-button">Выйти</button>
    );
};

export default LogoutButton;