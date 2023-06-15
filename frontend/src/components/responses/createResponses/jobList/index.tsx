import React, {useEffect, useRef, useState} from 'react';
import axios from "../../../../api/axios";
import CreateResponseFormComponent from "../createResponseForm";
import {Job} from "../../interfaces";


const JobListComponent = () => {
    const [jobs, setJobs] = useState<Job[]>([]);
    const errRef = useRef<HTMLDivElement>(null);
    const [errMsg, setErrMsg] = useState('');

    useEffect(() => {
        const getJobs = async () => {
            try {
                const jobs = await axios.get('/jobs');
                setJobs(jobs.data);
            } catch (err: any) {
                if (!err?.response) {
                    setErrMsg('Сервер не отвечает');
                }
                if (errRef.current) {
                    errRef.current.focus();
                }

            }
        };

        getJobs();
    }, []);

    return (
        <section>
            <h1>Оставить отклик</h1>
            <p ref={errRef} className={errMsg ? "errmsg" : "offscreen"} aria-live="assertive">
                {errMsg}
            </p>
            {jobs.map((job, index) => (
                <CreateResponseFormComponent
                    key={index}
                    id={job.id}
                    user_id={job.user_id}
                    title={job.title}
                    description={job.description}
                    salary_from={job.salary_from}
                    salary_to={job.salary_to}
                />
            ))}
        </section>
    );
};

export default JobListComponent;
