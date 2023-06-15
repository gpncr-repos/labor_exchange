import React, {useRef, useState} from 'react';
import useAuth from "../../../hooks/useAuth";
import {useNavigate} from "react-router-dom";
import axios from "../../../api/axiosPrivate";
import "../styles.css"

const UpdateDataComponent = () => {
    const {auth, setAuth} = useAuth();
    const navigate = useNavigate()
    const [username, setUsername] = useState(auth.name || '');
    const [email, setEmail] = useState(auth.email || '');
    const [password, setPassword] = useState('');
    const errRef = useRef<HTMLDivElement>(null);
    const [errMsg, setErrMsg] = useState('');
    console.log(auth)
    const handleUpdateData = async (event: any) => {
        event.preventDefault();

        try {
            await axios.put('/users', {
                name: username,
                email: email,
                password: password
            });
            setErrMsg('');


            //TODO: СДЕЛАТЬ АВТОРИЗАЦИЮ ПОСЛЕ ОБНОВЛЕНИЯ!!!!!!!!!!!!!
            setAuth({});
            localStorage.setItem('auth', JSON.stringify({}));
            navigate("/auth")


        } catch (err: any) {
            if (!err?.response) {
                setErrMsg('Сервер не отвечает');

            } else if (err.response?.status === 422) {
                setErrMsg('Некорректные данные');

            }
            if (errRef.current) {
                errRef.current.focus();
            }
        }
    }

    return (
        <section className="account-form-container">
            <h2>Изменить данные</h2>
            <p ref={errRef} className={errMsg ? "errmsg" : "offscreen"} aria-live="assertive">
                {errMsg}
            </p>

            <form className="account-form" onSubmit={handleUpdateData}>
                <label htmlFor="name">Имя пользователя:</label>
                <input
                    defaultValue={auth.username}
                    type="text"
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="Name"
                    id="name"
                    name="name"
                />

                <label htmlFor="email">Электронная почта:</label>
                <input
                    type="email"
                    defaultValue={auth.email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="emailexample@gmail.com"
                    id="email"
                    name="email"
                />

                <label htmlFor="password">Пароль:</label>
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="*******"
                    id="password"
                    name="password"
                    minLength={8}
                    required
                />

                <button type="submit">Обновить</button>
            </form>
        </section>
    );
};

export default UpdateDataComponent;