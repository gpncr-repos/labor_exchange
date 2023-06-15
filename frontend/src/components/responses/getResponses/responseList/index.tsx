import React, { useEffect, useRef, useState } from 'react';
import axios from '../../../../api/axios';
import ResponseItemComponent from '../responseItem';
import { UserData, Response, Job } from '../../interfaces';

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
    <section>

      <h2>Отклики</h2>
      <p ref={errRef} className={errMsg ? 'errmsg' : 'offscreen'} aria-live="assertive">
        {errMsg}
      </p>
      {responses.map((response, index) => {
        const matchingJob = jobs.find((job) => job.id === response.job_id);

        if (matchingJob) {
          return (

            <ResponseItemComponent
              key={index}
              response={response}
              job={matchingJob}
            />

          );
        }

        return null;
      })}
    </section>
  );
};

export default ResponsesListComponent;