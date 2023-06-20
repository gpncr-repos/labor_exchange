export interface UserData {
    id: number;
}

export interface Job {
    id: number;
    user_id: number;
    title: string;
    description: string;
    salary_from: number;
    salary_to: number;
}