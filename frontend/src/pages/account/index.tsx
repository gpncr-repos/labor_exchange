import React from 'react';
import LogoutButton from "../../components/auth/logoutButton";
import "../styles.css"
import UpdateDataComponent from "../../components/account/updateData";
import UpdatePasswordComponent from "../../components/account/updatePassword";

const AccountPage = () => {

    return (
        <section className="my-account">
            <h1>Мой аккаунт</h1>
            <div className="account-settings">
                <UpdateDataComponent/>
                <UpdatePasswordComponent/>
            </div>
            <LogoutButton/>
        </section>
    );
};

export default AccountPage;
