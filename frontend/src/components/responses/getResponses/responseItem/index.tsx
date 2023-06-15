import React from 'react';
import { Job, Response } from '../../interfaces';

interface ResponseComponentProps {
  response: Response;
  job: Job;
}

const ResponseItemComponent = ({ response, job }: ResponseComponentProps) => {
  return (
    <section>
      <h2>Вакансия:</h2>
      <p>Title: {job.title}</p>
      <p>Description: {job.description}</p>
      <p>Salary From: {job.salary_from}</p>
      <p>Salary To: {job.salary_to}</p>
      <h2>Ваш отклик</h2>
      <p>{response.message}</p>
    </section>
  );
};

export default ResponseItemComponent;
