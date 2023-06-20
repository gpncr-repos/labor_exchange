import React, {useRef, useState} from 'react';
import axios from "../../../../api/axiosPrivate";
import {Job} from "../../interfaces";
import "../../styles.css"

const CreateResponseFormComponent = ({id, user_id, title, description, salary_from, salary_to}: Job) => {
    const [message, setMessage] = useState('')
    const errRef = useRef<HTMLDivElement>(null);
    const [errMsg, setErrMsg] = useState('');

    const handleSubmit = async (e: any) => {
        e.preventDefault();
        try {
            await axios.post("/responses",
                JSON.stringify({
                        job_id: id,
                        message: message
                    }
                ),
                {
                    headers: {'Content-Type': 'application/json'},
                    withCredentials: true
                }
            )
            window.location.reload();
        } catch (err: any) {
            if (err.response?.status === 400) {
                setErrMsg('Вы уже оставили отклик на эту вакансию');
            }
            if (errRef.current) {
                errRef.current.focus();
            }
        }
    }

    return (
        <section className="create-response-form">
            <p ref={errRef} className={errMsg ? "errmsg" : "offscreen"} aria-live="assertive">
                {errMsg}
            </p>
            <h3 className="create-response-form__title">{title}</h3>
            <p className="create-response-form__description">{description}</p>
            <p className="create-response-form__salary">{salary_from} - {salary_to} ₽</p>

            <form onSubmit={handleSubmit} className="create-response-form__form">
                    <label htmlFor="message">Откликнуться на вакансию:</label>
                    <textarea className="create-response-form__textarea"
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        placeholder="Напишите о себе" id="message" name="message"
                    />
                    <button type="submit">Отправить</button>
            </form>
        </section>
    );
};

export default CreateResponseFormComponent;