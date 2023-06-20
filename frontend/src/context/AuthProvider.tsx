import React, {createContext, useState, ReactNode, useEffect} from "react";
import jwt_decode from 'jwt-decode';

const AuthContext = createContext<any>({});

interface AuthData {
  id: number | null;
  is_company: boolean;
  accessToken: string;
}

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const savedAuth = localStorage.getItem('auth');
  const initialAuth = savedAuth ? JSON.parse(savedAuth) : { id: null, is_company: false, accessToken: '' };
  const [auth, setAuth] = useState<AuthData>(initialAuth);
  const [isTokenExpired, setIsTokenExpired] = useState<boolean>(false);

  useEffect(() => {
    const checkTokenExpiration = () => {
      const accessToken = auth.accessToken;
      if (accessToken) {
        const decodedToken = jwt_decode<any>(accessToken);
        const currentTime = Date.now() / 1000;
        if (decodedToken.exp < currentTime) {
          setIsTokenExpired(true);
          setAuth({ id: null, is_company: false, accessToken: '' } );
          localStorage.removeItem('auth');
        } else {
          setIsTokenExpired(false);
        }
      }
    };

    checkTokenExpiration();
  }, [auth, isTokenExpired]);

  return (
    <AuthContext.Provider value={{ auth, setAuth }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;