import React from 'react';
import { Job, Response } from '../../interfaces';
import "../../styles.css"

interface ResponseComponentProps {
  response: Response;
  job: Job;
}

const ResponseItemComponent = ({ response, job }: ResponseComponentProps) => {
  return (
    <section className="job-item">
      <h3 className="job-item__title">Вакансия: {job.title}</h3>
      <p className="job-item__description">{job.description}</p>
      <p className="job-item__salary">{job.salary_from} - {job.salary_to} ₽</p>
      <h3>Ваш ответ</h3>
      <p>{response.message}</p>
    </section>
  );
};

export default ResponseItemComponent;
