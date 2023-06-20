import React, { useEffect, useRef, useState } from 'react';
import useAuth from '../../../hooks/useAuth';
import { useNavigate } from 'react-router-dom';
import axios from '../../../api/axiosPrivate';
import '../styles.css';

interface FormErrors {
  name?: string;
  email?: string;
  password?: string;
}

const UpdateDataComponent = () => {
  const { setAuth } = useAuth();
  const navigate = useNavigate();

  const initialValues = { name: '', email: '', password: '' };
  const [formValues, setFormValues] = useState(initialValues);
  const [formErrors, setFormErrors] = useState<FormErrors>({});
  const [isSubmit, setIsSubmit] = useState(false);
  const [errMsg, setErrMsg] = useState('');

  const handleChange = (event: any) => {
    const { name, value } = event.target;
    setFormValues({ ...formValues, [name]: value });
  };

  const validate = (values: any) => {
    const errors: FormErrors = {};
    const regex = /^[\w.-]+@([\w-]+\.)+[\w-]{2,4}$/;

    if (values.email === '' && values.name === '') {
      errors.name = 'Нужно изменить хотя бы одно поле'
      errors.email = 'Нужно изменить хотя бы одно поле'
    }
    if (!regex.test(values.email) && values.email !== '') {
      errors.email = 'Не правильный формат электронной почты!';
    }
    if (values.password.length < 8) {
      errors.password = 'Пароль должен быть не менее 8 символов!';
    } else if (values.password.length > 20) {
      errors.password = 'Пароль должен быть не более 20 символов!';
    }
    return errors;
  };

  const handleUpdateData = async (event: any) => {
    event.preventDefault();
    setIsSubmit(true);

    const errors = validate(formValues);
    setFormErrors(errors);

    try {
      if (Object.keys(errors).length === 0) {
        const requestData = {
          name: formValues.name ? formValues.name : null,
          email: formValues.email ? formValues.email : null,
        };

        await axios.put('/users', requestData);
        setErrMsg('');

        // TODO: СДЕЛАТЬ АВТОРИЗАЦИЮ ПОСЛЕ ОБНОВЛЕНИЯ!!!!!!!!!!!!!
        setAuth({});
        localStorage.setItem('auth', JSON.stringify({}));
        navigate('/auth');
      }
    } catch (err: any) {
      if (!err?.response) {
        setErrMsg('Сервер не отвечает');
      }else if (err.response?.status === 401) {
                setErrMsg('Неверный логин или пароль')
            }
    }
  };

  useEffect(() => {
    if (Object.keys(formErrors).length === 0 && isSubmit) {
      console.log(formValues);
    }
  }, [formValues]);

  return (
    <section className="account-form-container">
      <h2>Изменить данные</h2>
      {errMsg && <p className="errmsg">{errMsg}</p>}

      <form className="account-form" onSubmit={handleUpdateData}>
        <label htmlFor="name">Имя пользователя:</label>
        <input
          value={formValues.name}
          type="text"
          onChange={handleChange}
          placeholder="Name"
          id="name"
          name="name"
        />
        <p className="error-message">{formErrors.name}</p>
        <label htmlFor="email">Электронная почта:</label>
        <input
          type="text"
          value={formValues.email}
          onChange={handleChange}
          placeholder="emailexample@gmail.com"
          id="email"
          name="email"
        />
        <p className="error-message">{formErrors.email}</p>
        <label htmlFor="password">Пароль:</label>
        <input
          type="password"
          value={formValues.password}
          onChange={handleChange}
          placeholder="*******"
          id="password"
          name="password"
        />
        <p className="error-message">{formErrors.password}</p>
        <button type="submit">Обновить</button>
      </form>
    </section>
  );
};

export default UpdateDataComponent;
