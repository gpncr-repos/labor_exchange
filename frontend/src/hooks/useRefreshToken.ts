import useAuth from "./useAuth";
import axios from "../api/axios";

const UseRefreshToken = () => {
    const { auth, setAuth } = useAuth()
    const refresh = async () => {
        const response = await axios.post(`auth/refresh?token=${auth.accessToken}`, {
            withCredentials: true
        })
        setAuth((prev: any) => {
            console.log(prev.accessToken)
            console.log(response.data.access_token)
            return {
                ...prev,
                accessToken: response.data.access_token}
        })
        return response.data.access_token;
    }
    return refresh;
};

export default UseRefreshToken;