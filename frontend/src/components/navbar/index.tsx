import React from 'react';
import {Link, NavLink} from 'react-router-dom';
import useAuth from '../../hooks/useAuth';
import './styles.css';

const NavbarComponent: React.FC = () => {

    const {auth} = useAuth();
    const storage = localStorage.getItem("auth");
    const isCompany = storage !== null ? JSON.parse(storage).is_company : null;
    const isToken = auth.accessToken
    const isCompanyNavigation = () => {
        if (isToken && !isCompany) {
            return (
                <Link to="/responses" className="nav-links">Ваши отклики</Link>
            );
        } else if (isToken && isCompany) {
            return (
                <Link to="/jobs" className="nav-links">Ваши вакансии</Link>
            );
        }
    };

    const renderAccountButton = () => {
        if (isToken) {
            return (
                <Link to="/account">
                    <button className="btn">Аккаунт</button>
                </Link>
            );
        } else {
            return (
                <Link to="/auth">
                    <button className="btn">Авторизация</button>
                </Link>
            );
        }
    };

    return (
        <nav className="NavbarItems">
            <h1 className="navbar-logo">
                HH<i className="fa-solid fa-pen"></i>
            </h1>
            <ul className={'nav-menu'}>
                <li>
                    <NavLink to="/" className="nav-links">Главная</NavLink>
                </li>
            </ul>
            {isCompanyNavigation()}
            {renderAccountButton()}
        </nav>
    );
};

export default NavbarComponent;
