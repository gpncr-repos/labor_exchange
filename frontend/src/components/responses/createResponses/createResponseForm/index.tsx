import React, {useRef, useState} from 'react';
import axios from "../../../../api/axiosPrivate";
import {Job} from "../../interfaces";

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
        <section>
            <p ref={errRef} className={errMsg ? "errmsg" : "offscreen"} aria-live="assertive">
                {errMsg}
            </p>
            <h2>User ID: {user_id}</h2>
            <h3>Title: {title}</h3>
            <p>Description: {description}</p>
            <p>Salary: {salary_from} - {salary_to}</p>

            <form onSubmit={handleSubmit}>
                <label htmlFor="message">Заголовок</label>
                <input
                    type="text"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    id="message"
                />
                <button type="submit">Отправить</button>
            </form>
        </section>
    );
};

export default CreateResponseFormComponent;