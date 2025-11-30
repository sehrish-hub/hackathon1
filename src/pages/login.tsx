import React from 'react';
import Layout from '@theme/Layout';

function LoginPage() {
  return (
    <Layout
      title="Sign In"
      description="Login page for Docusaurus application"
    >
      <main className="container my-auto">
        <div className="row justify-content-center">
          <div className="col-md-6 col-lg-4">
            <h1 className="text--center">Sign In</h1>
            <form>
              <div className="margin-bottom--md">
                <label htmlFor="username">Username</label>
                <input
                  type="text"
                  id="username"
                  name="username"
                  className="form-control"
                  placeholder="Enter your username"
                  required
                />
              </div>
              <div className="margin-bottom--md">
                <label htmlFor="password">Password</label>
                <input
                  type="password"
                  id="password"
                  name="password"
                  className="form-control"
                  placeholder="Enter your password"
                  required
                />
              </div>
              <button type="submit" className="button button--primary button--block">
                Sign In
              </button>
            </form>
          </div>
        </div>
      </main>
    </Layout>
  );
}

export default LoginPage;