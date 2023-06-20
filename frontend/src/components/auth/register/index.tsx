import React, {useEffect, useState} from 'react';
import axios from '../../../api/axios';
import '../styles.css';
import {useLocation, useNavigate} from "react-router-dom";
import useAuth from "../../../hooks/useAuth";

interface FormErrors {
    name?: string,
    email?: string,
    password?: string,
    password2?: string,
    isCompany?: boolean
}

const RegisterComponent = (props: any) => {
    const { setAuth } = useAuth()
    const navigate = useNavigate()
    const location = useLocation();
    const from = location.state?.from?.pathname || "/"

    const initialValues = {name: '', email: '', password: '', password2: '', isCompany: false}
    const [formValues, setFormValues] = useState(initialValues)
    const [formErrors, setFormErrors] = useState<FormErrors>({})
    const [isSubmit, setIsSubmit] = useState(false);
    const [errMsg, setErrMsg] = useState('');

    const handleChange = (event: any) => {
        const {name, value} = event.target;
        setFormValues({...formValues, [name]: value});
    }

    const handleSubmit = async (event: any) => {
        event.preventDefault();
        setFormErrors(validate(formValues))
        setIsSubmit(true)

        try {
            await axios.post('/users', {
                name: formValues.name,
                email: formValues.email,
                password: formValues.password,
                password2: formValues.password2,
                is_company: formValues.isCompany,
            });


            const loginResponse = await axios.post('/auth', {
                email: formValues.email,
                password: formValues.password,
            });
            const {id: id, access_token: accessToken, is_company: is_company } = loginResponse?.data;

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
            }
        }
    };

    useEffect(() => {
        if (Object.keys(formErrors).length === 0 && isSubmit) {
            console.log(formValues)
        }
    }, [formValues])

    const validate = (values: any) => {
        const errors: FormErrors = {};
        const regex = /^[\w.-]+@([\w-]+\.)+[\w-]{2,4}$/;
        if (!values.name) {
            errors.name = "Имя - это обязательное поле!"
        }
        if (!values.email) {
            errors.email = "Email - это обязательное поле!"
        } else if (!regex.test(values.email)) {
            errors.email = "Не правильный формат электронной почты!"
        }
        if (!values.password) {
            errors.password = "Пароль - это обязательное поле!"
        }else if (values.password.length < 8) {
            errors.password = "Пароль должен быть не менее 8 символов!"
        }else if (values.password.length > 20) {
            errors.password = "Пароль должен быть не более 20 символов!"
        }
        if (!values.password2) {
            errors.password2 = "Пароль - это обязательное поле!"
        }else if (values.password !== values.password2){
            errors.password2 = "Пароли не совпадают!"
        }
        return errors;
    }
    return (
        <section className="auth-form-container">
            <h1>Регистрация</h1>
            {errMsg && <p className="errmsg">{errMsg}</p>}
            <form className="register-form" onSubmit={handleSubmit}>
                <label htmlFor="name">Имя</label>
                <input
                    value={formValues.name}
                    type="text"
                    onChange={handleChange}
                    placeholder="Name"
                    id="name"
                    name="name"
                />
                <p className="error-message">{formErrors.name}</p>
                <label htmlFor="email">Email</label>
                <input
                    value={formValues.email}
                    type="text"
                    onChange={handleChange}
                    placeholder="emailexample@gmail.com"
                    id="email"
                    name="email"
                />
                <p className="error-message">{formErrors.email}</p>
                <label htmlFor="password">Пароль</label>
                <input
                    value={formValues.password}
                    type="password"
                    onChange={handleChange}
                    placeholder="*******"
                    id="password"
                    name="password"
                />
                <p className="error-message">{formErrors.password}</p>
                <label htmlFor="password2">Повторите пароль</label>
                <input
                    value={formValues.password2}
                    type="password"
                    onChange={handleChange}
                    placeholder="*******"
                    id="password2"
                    name="password2"
                />
                <p className="error-message">{formErrors.password2}</p>
                <div className="company-label">
                    <label htmlFor="isCompany">Представитель компании?</label>
                    <input
                        className="company-checkbox"
                        type="checkbox"
                        checked={formValues.isCompany}
                        onChange={handleChange}
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
