import React, {useEffect, useRef, useState} from 'react';
import axios from "../../../../api/axios";
import {UserData} from "../../interfaces";
import "../../styles.css"
import JobItemComponent from "../jobItem";

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
        <section className="job-list-container">
            <h2 className="job-list__name">Список Ваших вакансий</h2>
            <p ref={errRef} className={errMsg ? "errmsg" : "offscreen"} aria-live="assertive">{errMsg}</p>
            <div style={{height: '800px', overflowY: 'scroll', scrollbarWidth: 'thin'}}>
                {filteredJobs.map((job, index) => {
                    return (
                        <JobItemComponent
                            key={index}
                            job={job}
                        />
                    )
                })}
            </div>
        </section>
    );
};

export default JobListComponent;