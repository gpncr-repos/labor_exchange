import React, { useState, useEffect } from 'react';
import JobListComponent from "../../components/jobs/getJobs/jobList";
import CreateJobFormComponent from "../../components/jobs/createJobs/createJobForm";
import "../styles.css"

const JobPage = () => {
    return (
        <section className="my-jobs">
            <h1>Вакансии</h1>
            <div className="jobs-settings">
                <CreateJobFormComponent />
                <JobListComponent />
            </div>
        </section>
    );
};

export default JobPage;
