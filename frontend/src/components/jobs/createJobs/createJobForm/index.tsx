import React, {useState, useEffect, useRef} from 'react';
import axios from "../../../../api/axiosPrivate";
import "../../styles.css"

const CreateJobFormComponent = () => {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [salaryFrom, setSalaryFrom] = useState('');
    const [salaryTo, setSalaryTo] = useState('');

    const errRef = useRef<HTMLDivElement>(null);
    const [errMsg, setErrMsg] = useState('')

    useEffect(() => {
        setSalaryTo(salaryFrom);
    }, [salaryFrom]);

    const handleSubmit = async (e: any) => {
        e.preventDefault();
        try {
            await axios.post('/jobs',
                JSON.stringify({
                        title: title,
                        description: description,
                        salary_from: salaryFrom,
                        salary_to: salaryTo
                    }
                ),
                {
                    headers: {'Content-Type': 'application/json'},
                    withCredentials: true
                }
            );
            window.location.reload();
        } catch (err: any) {
            if (!err?.response) {
                setErrMsg('Сервер не отвечает');
            } else if (parseInt(salaryFrom) < 0 || parseInt(salaryTo) < 0) {
                setErrMsg('Зарплата не может быть меньше нуля')
            } else if (err.response?.status === 422) {
                setErrMsg('Некорректные данные')
            }
            if (errRef.current) {
                errRef.current.focus();
            }
        }
        setTitle('')
        setDescription('')
        setSalaryFrom('')
        setSalaryTo('')
    };

    return (
        <section className="create-job-form-container">
            <h2 className="create-job-form__name">Создать новую вакансию</h2>
            <p ref={errRef} className={errMsg ? "errmsg" : "offscreen"} aria-live="assertive">{errMsg}</p>
            <form className="create-job-form" onSubmit={handleSubmit}>
                <label htmlFor="title">Заголовок</label>
                <input
                    type="text"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    id="title"
                />
                <label htmlFor="description">Описание</label>
                <textarea className="create-job-form__textarea"
                          value={description}
                          onChange={(e) => setDescription(e.target.value)}
                          placeholder="Расскажите о Вашей вакансии..." id="description" name="description"
                />
                <div className="job-salary-form">
                    <div className="create-job-form__salary-from">
                        <label htmlFor="salary-from">Зарплата от</label>
                        <input
                            type="number"
                            min="0"
                            max="1000000"
                            step="1"
                            value={salaryFrom}
                            onChange={(e) => setSalaryFrom(e.target.value)}
                            id="salary-from"
                        />
                    </div>
                    <div className="create-job-form__salary-to">
                        <label htmlFor="salary-to">Зарплата до</label>
                        <input
                            type="number"
                            min={salaryFrom}
                            max="1000000"
                            step="1"
                            value={salaryTo}
                            onChange={(e) => setSalaryTo(e.target.value)}
                            id="salary-to"
                        />
                    </div>
                </div>
                <button type="submit">Создать</button>
            </form>
        </section>
    );
};

export default CreateJobFormComponent;
