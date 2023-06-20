import React, { useEffect, useRef, useState } from 'react';
import axios from '../../../../api/axios';
import CreateResponseFormComponent from '../createResponseForm';
import { Job } from '../../interfaces';
import "../../styles.css"

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
    <section className="job-list-container">
      <h2 className="response-list-container__name">Оставить отклик</h2>
      <p ref={errRef} className={errMsg ? 'errmsg' : 'offscreen'} aria-live="assertive">
        {errMsg}
      </p>
      <div style={{ height: '50rem', overflowY: 'scroll', scrollbarWidth: 'thin' }}>
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
      </div>
    </section>
  );
};

export default JobListComponent;