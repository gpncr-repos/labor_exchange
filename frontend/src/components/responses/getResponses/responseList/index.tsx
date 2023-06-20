import React, { useEffect, useRef, useState } from 'react';
import axios from '../../../../api/axios';
import ResponseItemComponent from '../responseItem';
import { UserData, Response, Job } from '../../interfaces';
import "../../styles.css"

const ResponsesListComponent = () => {
  const [responses, setResponses] = useState<Response[]>([]);
  const [jobs, setJobs] = useState<Job[]>([]);
  const errRef = useRef<HTMLDivElement>(null);
  const [errMsg, setErrMsg] = useState('');

  const storage = localStorage.getItem('auth');
  const userData: UserData | null = storage ? JSON.parse(storage) : null;

  useEffect(() => {
    const getResponses = async () => {
      try {

        const responses = await axios.get(`/responses/user-id/${userData?.id}`);
        setResponses(responses.data);

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

    getResponses();
  }, []);

  return (
    <section className="response-list-container">
      <h2 className="response-list-container__name">Ваши отклики</h2>
      <p ref={errRef} className={errMsg ? 'errmsg' : 'offscreen'} aria-live="assertive">
        {errMsg}
      </p>
      <div style={{ height: '50rem', overflowY: 'scroll', scrollbarWidth: 'thin' }}>
      {responses.map((response, index) => {
        const filteredJob = jobs.find((job) => job.id === response.job_id);

        if (filteredJob) {
          return (

            <ResponseItemComponent
              key={index}
              response={response}
              job={filteredJob}
            />

          );
        }

        return null;
      })}
      </div>
    </section>
  );
};

export default ResponsesListComponent;