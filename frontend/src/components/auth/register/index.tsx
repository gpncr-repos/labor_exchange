import React, {useState} from 'react';
import axios from '../../../api/axios';
import '../styles.css';
import {useLocation, useNavigate} from "react-router-dom";
import useAuth from "../../../hooks/useAuth";

const RegisterComponent = (props: any) => {
    const navigate = useNavigate()
    const location = useLocation();
    const from = location.state?.from?.pathname || "/"
    const { setAuth } = useAuth()
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [password2, setPassword2] = useState('');
    const [isCompany, setIsCompany] = useState(false);
    const [errMsg, setErrMsg] = useState('');

    const handleSubmit = async (event: any) => {
        event.preventDefault();

        try {
            await axios.post('/users', {
                name: name,
                email: email,
                password: password,
                password2: password2,
                is_company: isCompany,
            });


            const loginResponse = await axios.post('/auth', {
                email: email,
                password: password,
            });
            const {id: id, access_token: accessToken, is_company: is_company } = loginResponse?.data;

            setAuth({
                email: email,
                password: password,
                accessToken: accessToken,
            });

            localStorage.setItem('auth', JSON.stringify({
                id: id,
                is_company: is_company,
                accessToken: accessToken,

            }));

            setName('');
            setEmail('');
            setPassword('');
            setPassword2('');
            setIsCompany(false);
            navigate(from, {replace: true})

        } catch (err: any) {
            setErrMsg('Регистрация не удалась');
        }
    };

    return (
        <section className="auth-form-container">
            <h1>Регистрация</h1>
            {errMsg && <p className="errmsg">{errMsg}</p>}
            <form className="register-form" onSubmit={handleSubmit}>
                <label htmlFor="name">Имя</label>
                <input
                    value={name}
                    type="text"
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Name"
                    id="name"
                    name="name"
                    required
                />
                <label htmlFor="email">Email</label>
                <input
                    value={email}
                    type="email"
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="emailexample@gmail.com"
                    id="email"
                    name="email"
                    required
                />
                <label htmlFor="password">Пароль</label>
                <input
                    value={password}
                    type="password"
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="*******"
                    id="password"
                    name="password"
                    required
                />
                <label htmlFor="password2">Повторите пароль</label>
                <input
                    value={password2}
                    type="password"
                    onChange={(e) => setPassword2(e.target.value)}
                    placeholder="*******"
                    id="password2"
                    name="password2"
                    required
                />
                <div className="company-label">
                    <label htmlFor="isCompany">Представитель компании?</label>
                    <input
                        className="company-checkbox"
                        type="checkbox"
                        checked={isCompany}
                        onChange={(e) => setIsCompany(e.target.checked)}
                        id="isCompany"
                        name="isCompany"
                    />
                </div>
                <button type="submit">Зарегистрироваться</button>
            </form>
            <div>
                Уже есть аккаунт?
                <button className="link-btn" onClick={() => props.onFormSwitch('login')}>Авторизуйтесь</button>
            </div>
        </section>
    );
};

export default RegisterComponent;
