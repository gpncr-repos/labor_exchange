import React from 'react';
import {Outlet} from "react-router-dom";
import NavbarComponent from "../navbar";

const Layout = () => {
    return (
        <main className="App">
            <NavbarComponent />
            <Outlet />
        </main>
    );
};

export default Layout;