export interface Job {
    id: number;
    user_id: number;
    title: string;
    description: string;
    salary_from: number;
    salary_to: number;
}

export interface Response {
    user_id: number
    job_id: number;
    message: string;
}

export interface UserData {
    id: number;
}