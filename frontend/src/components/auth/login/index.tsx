import React, {useRef, useState} from 'react';
import "../styles.css"

import axios from "../../../api/axios";
import {useLocation, useNavigate} from "react-router-dom";
import useAuth from "../../../hooks/useAuth";

const LoginComponent = (props: any) => {
    const { setAuth } = useAuth()

    const navigate = useNavigate();
    const location = useLocation();
    const errRef = useRef<HTMLDivElement>(null);

    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [errMsg, setErrMsg] = useState('')

    const from = location.state?.from?.pathname || "/"

    const handleSubmit = async (event: any) => {
        event.preventDefault()
        try {

            const response = await axios.post('/auth',
                JSON.stringify({email: email, password: password}),
                {
                    headers: {'Content-Type': 'application/json'},
                    withCredentials: true
                }
            );

            const { id: id, access_token: accessToken, is_company: is_company } = response?.data;
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

            setEmail('')
            setPassword('')
            navigate(from, {replace: true})

        } catch (err: any) {
            if (!err?.response) {
                setErrMsg('Сервер не отвечает');
            } else if (email === '' || password === '') {
                setErrMsg('Заполните все поля')
            } else if (err.response?.status === 401) {
                setErrMsg('Неверный логин или пароль')
            }
            if (errRef.current) {
                errRef.current.focus();
            }
        }
    }

    return (

        <section className="auth-form-container">
            <h1>Вход</h1>
            <p ref={errRef} className={errMsg ? "errmsg" : "offscreen"} aria-live="assertive">{errMsg}</p>
            <form className="login-form" onSubmit={handleSubmit}>
                <label htmlFor="email">Email</label>
                <input
                    value={email}
                    type="email"
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="emailexample@gmail.com" id="email" name="email"/>
                <label htmlFor="password">Пароль</label>
                <input
                    value={password}
                    type="password"
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="*******" id="password" name="password"/>
                <button type="submit">Войти</button>
            </form>
            <div>
                У Вас нет учётной записи?
                <button className="link-btn" onClick={() => props.onFormSwitch('register')}>Зарегистрируйтесь</button>
            </div>
        </section>
    )
}


export default LoginComponent;