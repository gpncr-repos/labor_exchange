import React from 'react';
import { Job } from '../../interfaces';

const JobItemComponent = ({ job }: { job: Job }) => {
  return (
    <section className="job-item">
      <h3 className="job-item__title">Вакансия: {job.title}</h3>
      <p className="job-item__description">{job.description}</p>
      <p className="job-item__salary">
        {job.salary_from} - {job.salary_to} ₽
      </p>
    </section>
  );
};

export default JobItemComponent;