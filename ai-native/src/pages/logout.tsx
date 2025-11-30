import React, {useEffect} from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import styles from './login.module.css';

export default function Logout(): JSX.Element {
  useEffect(() => {
    try {
      // Clear any client-side auth tokens (UI-only). This is harmless if none exist.
      localStorage.removeItem('authToken');
      sessionStorage.removeItem('authToken');
    } catch (e) {
      // Ignore storage errors in some environments
    }

    // Redirect to homepage after a short delay to give feedback
    const t = setTimeout(() => {
      window.location.href = '/';
    }, 900);
    return () => clearTimeout(t);
  }, []);

  return (
    <Layout title="Signed out" description="You have been signed out">
      <main className={styles.root}>
        <div className={styles.card} role="status" aria-live="polite">
          <img src="/img/logo.svg" alt="AI Native" className={styles.logo} />
          <h1 className={styles.title}>Signed Out</h1>
          <p className={styles.subtitle}>You have been signed out. Redirecting to the homepage…</p>
          <div style={{marginTop: 12}}>
            <Link className={styles.button} to="/login">
              Go to Sign In
            </Link>
          </div>
        </div>
      </main>
    </Layout>
  );
}
