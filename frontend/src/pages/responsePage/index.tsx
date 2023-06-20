import React from 'react';
import JobListComponent from "../../components/responses/createResponses/jobList";
import ResponsesListComponent from "../../components/responses/getResponses/responseList";
import "../styles.css"

const ResponsePage = () => {
    return (
        <section className="my-responses">
            <h1>Отклики на вакансии</h1>
            <div className="responses-settings">
                <JobListComponent/>
                <ResponsesListComponent/>
            </div>
        </section>
    );
};

export default ResponsePage;