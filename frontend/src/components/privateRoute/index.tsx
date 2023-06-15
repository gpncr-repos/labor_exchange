import { useLocation, Navigate, Outlet } from "react-router-dom";
import React from "react";
import useAuth from "../../hooks/useAuth";

const PrivateRoute = () => {
  const { auth } = useAuth();
  const location = useLocation();

  return auth?.accessToken ? <Outlet /> : <Navigate to="/auth" state={{ from: location }} replace />;
};

export default PrivateRoute;