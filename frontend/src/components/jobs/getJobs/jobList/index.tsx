import React, {useEffect, useRef, useState} from 'react';
import axios from "../../../../api/axios";
import {UserData} from "../../interfaces";
const JobListComponent = () => {
    const [jobs, setJobs] = useState<any[]>([]);
    const storage = localStorage.getItem("auth");
    const userData: UserData | null = storage ? JSON.parse(storage) : null;

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

    const filteredJobs = jobs.filter(job => job?.user_id === userData?.id);

    return (
        <section>
            <h2>Список Ваших вакансий</h2>
            <p ref={errRef} className={errMsg ? "errmsg" : "offscreen"} aria-live="assertive">{errMsg}</p>
            {filteredJobs.length ? (
                <ul>
                    {filteredJobs.map((job, i) => (
                        <li key={i}>
                            {job?.user_id} {job?.title} {job?.description} {job?.salary_from} {job?.salary_to}
                        </li>
                    ))}
                </ul>
            ) : (
                <p>No users to display</p>
            )}
        </section>
    );
};

export default JobListComponent;