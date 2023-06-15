import React, { useState, useEffect } from 'react';
import JobListComponent from "../../components/jobs/getJobs/jobList";
import CreateJobFormComponent from "../../components/jobs/createJobs/createJobForm";
import "./styles.css"

const JobPage = () => {
    const [jobAdded, setJobAdded] = useState(false);

    useEffect(() => {
        if (jobAdded) {
            window.location.reload();
        }
    }, [jobAdded]);

    const handleJobAdded = () => {
        setJobAdded(true);
    };

    return (
        <section className="my-jobs">
            <h1>Вакансии</h1>
            <div className="jobs-settings">
                <CreateJobFormComponent onJobAdded={handleJobAdded} />
                <JobListComponent />
            </div>
        </section>
    );
};

export default JobPage;
