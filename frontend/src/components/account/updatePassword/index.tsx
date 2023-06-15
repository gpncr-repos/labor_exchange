import React, {useRef, useState} from 'react';
import axios from "../../../api/axiosPrivate";
import useAuth from "../../../hooks/useAuth";
import {useNavigate} from "react-router-dom";
import "../styles.css"

const UpdatePasswordComponent = () => {
    const {setAuth} = useAuth();
    const navigate = useNavigate()
    const [password, setPassword] = useState('');
    const [password2, setPassword2] = useState('');
    const [oldPassword, setOldPassword] = useState('');
    const errRef = useRef<HTMLDivElement>(null);
    const [errMsg, setErrMsg] = useState('');

    const handleUpdatePassword = async (event: any) => {
        event.preventDefault();

        try {

            if(password !== password2){
                setErrMsg('Пароли не совпадают');
            }else
            {
                await axios.put('/users', {
                    new_password: password,
                    password: oldPassword
                });
                setErrMsg('');



                //TODO: СДЕЛАТЬ АВТОРИЗАЦИЮ ПОСЛЕ ОБНОВЛЕНИЯ!!!!!!!!!!!!!
                setAuth({});
                localStorage.setItem('auth', JSON.stringify({}));
                navigate("/auth")



            }
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
            <h2>Изменить пароль</h2>
            <p ref={errRef} className={errMsg ? "errmsg" : "offscreen"} aria-live="assertive">
                {errMsg}
            </p>
            <form className="account-form" onSubmit={handleUpdatePassword}>
                <label htmlFor="newPassword">Новый пароль</label>
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="*******"
                    id="newPassword"
                    name="password"
                    minLength={8}
                    required
                />
                <label htmlFor="newPassword2">Подтвердите новый пароль</label>
                <input
                    type="password"
                    value={password2}
                    onChange={(e) => setPassword2(e.target.value)}
                    placeholder="*******"
                    id="newPassword2"
                    name="password2"
                    minLength={8}
                    required
                />
                <label htmlFor="oldPassword">Старый пароль</label>
                <input
                    type="password"
                    value={oldPassword}
                    onChange={(e) => setOldPassword(e.target.value)}
                    placeholder="*******"
                    id="oldPassword"
                    name="oldPassword"
                    minLength={8}
                    required
                />

                <button type="submit">Обновить</button>
            </form>
        </section>
    );
};

export default UpdatePasswordComponent;