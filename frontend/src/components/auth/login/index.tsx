import React, {useEffect, useRef, useState} from 'react';
import "../styles.css"

import axios from "../../../api/axios";
import {useLocation, useNavigate} from "react-router-dom";
import useAuth from "../../../hooks/useAuth";

interface FormErrors {
    email?: string;
    password?: string;
}

const LoginComponent = (props: any) => {
    const {setAuth} = useAuth()
    const navigate = useNavigate();
    const location = useLocation();
    const from = location.state?.from?.pathname || "/"

    const initialValues = {email: '', password: ''}
    const [formValues, setFormValues] = useState(initialValues)
    const [formErrors, setFormErrors] = useState<FormErrors>({});
    const [isSubmit, setIsSubmit] = useState(false);
    const [errMsg, setErrMsg] = useState('')


    const handleChange = (event: any) => {
        const {name, value} = event.target;
        setFormValues({...formValues, [name]: value});
    }

    const handleSubmit = async (event: any) => {
        event.preventDefault();
        setFormErrors(validate(formValues))
        setIsSubmit(true)

        try {

            const response = await axios.post('/auth',
                JSON.stringify({email: formValues.email, password: formValues.password}),
                {
                    headers: {'Content-Type': 'application/json'},
                    withCredentials: true
                }
            );

            const {id: id, access_token: accessToken, is_company: is_company} = response?.data;
            setAuth({
                email: formValues.email,
                password: formValues.password,
                accessToken: accessToken,
            });

            localStorage.setItem('auth', JSON.stringify({
                id: id,
                is_company: is_company,
                accessToken: accessToken,
            }));

            navigate(from, {replace: true})

        } catch (err: any) {
            if (!err?.response) {
                setErrMsg('Сервер не отвечает');
            }else if (err.response?.status === 401) {
                setErrMsg('Неверный логин или пароль')
            }

        }
    }

    useEffect(() => {
        if (Object.keys(formErrors).length === 0 && isSubmit) {
            console.log(formValues)
        }
    }, [formValues])

    const validate = (values: any) => {
        const errors: FormErrors = {};
        const regex = /^[\w.-]+@([\w-]+\.)+[\w-]{2,4}$/;
        if (!values.email) {
            errors.email = "Email - это обязательное поле!"
        } else if (!regex.test(values.email)) {
            errors.email = "Не правильный формат электронной почты!"
        }
        if (!values.password) {
            errors.password = "Пароль - это обязательное поле!"
        } else if (values.password.length < 8) {
            errors.password = "Пароль должен быть не менее 8 символов!"
        } else if (values.password.length > 20) {
            errors.password = "Пароль должен быть не более 20 символов!"
        }
        return errors;
    }

    return (
        <section className="auth-form-container">
            {errMsg && <p className="errmsg">{errMsg}</p>}
            <h1>Вход</h1>
            <form className="login-form" onSubmit={handleSubmit}>
                <label htmlFor="email">Email</label>
                <input
                    value={formValues.email}
                    type="text"
                    onChange={handleChange}
                    placeholder="emailexample@gmail.com" id="email" name="email"/>
                <p className="error-message">{formErrors.email}</p>
                <label htmlFor="password">Пароль</label>
                <input
                    value={formValues.password}
                    type="password"
                    onChange={handleChange}
                    placeholder="*******" id="password" name="password"/>
                <p className="error-message">{formErrors.password}</p>
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