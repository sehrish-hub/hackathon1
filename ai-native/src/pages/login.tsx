import React from 'react';
import Layout from '@theme/Layout';
import clsx from 'clsx';
import styles from './login.module.css';

function LoginPage() {
  return (
    <Layout title="Login" description="Login page">
      <div className={styles.root}>
        <div className={styles.card}>
          <h2 className={styles.title}>Sign In</h2>
          <p className={styles.subtitle}>Sign in to your account to continue</p>
          <form className={styles.form}>
          <div>
            <label htmlFor="username" className={styles.label}>Username:</label>
            <input
              type="text"
              id="username"
              name="username"
              placeholder="Enter your username"
              className={styles.input}
            />
          </div>
          <div>
            <label htmlFor="password" className={styles.label}>Password:</label>
            <input
              type="password"
              id="password"
              name="password"
              placeholder="Enter your password"
              className={styles.input}
            />
          </div>
          <button type="submit" className={styles.button}>
            Sign In
          </button>
                  </form>
                </div>
              </div>
            </Layout>
          );}

export default LoginPage;
