import React from 'react';
import JobListComponent from "../../components/responses/createResponses/jobList";
import ResponsesListComponent from "../../components/responses/getResponses/responseList";

const ResponsePage = () => {
    return (
        <>
            <JobListComponent/>
            <ResponsesListComponent/>
        </>
    );
};

export default ResponsePage;