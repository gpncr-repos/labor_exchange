import React, {useRef, useState} from 'react';
import axios from "../../../api/axiosPrivate";
import useAuth from "../../../hooks/useAuth";
import {useNavigate} from "react-router-dom";
import "../styles.css"

interface FormErrors {
    password?: string;
    password2?: string;
    oldPassword?: string;
}

const UpdatePasswordComponent = () => {
    const {setAuth} = useAuth();
    const navigate = useNavigate()

    const initialValues = {password: '', password2: '', oldPassword: ''};
    const [formValues, setFormValues] = useState(initialValues);
    const [formErrors, setFormErrors] = useState<FormErrors>({});
    const [isSubmit, setIsSubmit] = useState(false);
    const [errMsg, setErrMsg] = useState('');

    const handleChange = (event: any) => {
        const {name, value} = event.target;
        setFormValues({...formValues, [name]: value});
    };

    const validate = (values: any) => {
        const errors: FormErrors = {};
        if (!values.password){
            errors.password = 'Это обязательное поле!'
        }else if (values.password.length < 8) {
            errors.password = 'Пароль должен быть не менее 8 символов!';
        } else if (values.password.length > 20) {
            errors.password = 'Пароль должен быть не более 20 символов!';
        }

        if (!values.password2){
            errors.password2 = 'Это обязательное поле!'
        }else if (values.password !== values.password2){
            errors.password2 = 'Пароли не совпадают!'
        }

        if (!values.oldPassword){
            errors.oldPassword = 'Это обязательное поле!'
        }

        return errors;
    };

    const handleUpdatePassword = async (event: any) => {
        event.preventDefault();
        setIsSubmit(true);

        const errors = validate(formValues);
        setFormErrors(errors);

        try {

                await axios.put('/users', {
                    new_password: formValues.password,
                    password: formValues.oldPassword
                });
                setErrMsg('');


                //TODO: СДЕЛАТЬ АВТОРИЗАЦИЮ ПОСЛЕ ОБНОВЛЕНИЯ!!!!!!!!!!!!!
                setAuth({});
                localStorage.setItem('auth', JSON.stringify({}));
                navigate("/auth")

        } catch (err: any) {
            if (!err?.response) {
                setErrMsg('Сервер не отвечает');
            }else if (err.response?.status === 422) {
                setErrMsg('Неверный старый пароль')
            }
        }
    }

    return (
        <section className="account-form-container">
            <h2>Изменить пароль</h2>
            {errMsg && <p className="errmsg">{errMsg}</p>}

            <form className="account-form" onSubmit={handleUpdatePassword}>
                <label htmlFor="newPassword">Новый пароль</label>
                <input
                    type="password"
                    value={formValues.password}
                    onChange={handleChange}
                    placeholder="*******"
                    id="newPassword"
                    name="password"
                />
                <p className="error-message">{formErrors.password}</p>
                <label htmlFor="newPassword2">Подтвердите новый пароль</label>
                <input
                    type="password"
                    value={formValues.password2}
                    onChange={handleChange}
                    placeholder="*******"
                    id="newPassword2"
                    name="password2"
                />
                <p className="error-message">{formErrors.password2}</p>
                <label htmlFor="oldPassword">Старый пароль</label>
                <input
                    type="password"
                    value={formValues.oldPassword}
                    onChange={handleChange}
                    placeholder="*******"
                    id="oldPassword"
                    name="oldPassword"
                />
                <p className="error-message">{formErrors.oldPassword}</p>

                <button type="submit">Обновить</button>
            </form>
        </section>
    );
};

export default UpdatePasswordComponent;