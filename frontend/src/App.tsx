import React from 'react';
import './App.css';
import { Route, Routes } from 'react-router-dom';
import AuthPage from './pages/auth';
import HomePage from './pages/home';
import Layout from "./components/layout";
import PrivateRoute from "./components/privateRoute";
import AccountPage from "./pages/account";
import JobPage from "./pages/jobPage";
import ResponsePage from "./pages/responsePage";

function App() {
  return (
      <Routes>
          <Route path="/" element={<Layout />}>
            <Route path="/" element={<HomePage />} />
            <Route path="/auth" element={<AuthPage />} />
              <Route element={<PrivateRoute />}>
                  <Route path="/responses" element={<ResponsePage />} />
                  <Route path="/jobs" element={<JobPage />} />
                  <Route path="/account" element={<AccountPage />} />
              </Route>
          </Route>
      </Routes>
  );
}

export default App;