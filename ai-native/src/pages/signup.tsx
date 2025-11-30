import React from 'react';
import Layout from '@theme/Layout';

function SignUp() {
  return (
    <Layout title="Sign Up" description="Sign up for an account">
      <div className="flex items-center justify-center min-h-screen bg-gray-50 dark:bg-gray-900 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8 p-10 bg-white dark:bg-gray-800 rounded-lg shadow-xl">
          <div>
            <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900 dark:text-white">
              Create your account
            </h2>
          </div>

          <button
            type="button"
            className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition duration-150 ease-in-out"
          >
            <span className="absolute left-0 inset-y-0 flex items-center pl-3">
              <svg className="h-5 w-5 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12.000000000000002 4.60625C13.886363636363638 4.60625 15.285 5.305681818181818 16.14375 6.136363636363637L19.220454545454547 3.059659090909091C17.200568181818183 1.1448863636363638 14.712500000000002 0 12.000000000000002 0C7.271022727272727 0 3.1977272727272725 2.6914772727272725 1.1778409090909092 6.636818181818182L5.277840909090909 9.713636363636363C6.273863636363637 7.009090909090909 8.924431818181818 4.60625 12.000000000000002 4.60625Z" fill="#EA4335"/>
                <path d="M23.7046875 12.213802083333334C23.7046875 11.458932291666666 23.649999999999995 10.741067708333334 23.51328125 10.067317708333334H12V14.630208333333334H18.96640625C18.667708333333332 16.208932291666666 17.766119791666665 17.525520833333332 16.425 18.39765625L16.40833333333333 18.513020833333332L19.967708333333332 21.232552083333332L20.088020833333332 21.293489583333332C22.21953125 19.161458333333332 23.7046875 16.269791666666668 23.7046875 12.213802083333334Z" fill="#4285F4"/>
                <path d="M16.425 18.39765625L19.967708333333332 21.232552083333332C19.23125 21.748177083333332 18.472791666666666 22.18828125 17.683333333333334 22.55390625L17.625 22.5859375L13.784375 19.4140625L13.684375 19.347395833333332C12.923958333333332 19.529817708333332 12 19.645833333333332 12 19.645833333333332C8.924431818181818 19.645833333333332 6.273863636363637 17.243020833333332 5.277840909090909 14.538489583333332L1.1778409090909092 17.6153125C3.1977272727272725 21.560677083333332 7.271022727272727 24.252083333333332 12.000000000000002 24.252083333333332C14.712500000000002 24.252083333333332 17.200568181818183 23.1071875 19.220454545454547 21.19234375L16.425 18.39765625Z" fill="#FBBC04"/>
                <path d="M1.1778409090909092 6.636818181818182L5.277840909090909 9.713636363636363C4.945454545454545 10.613636363636363 4.75 11.583806818181819 4.75 12.585227272727273C4.75 13.586647727272727 4.945454545454545 14.556818181818182 5.277840909090909 15.456818181818182L1.1778409090909092 18.533636363636363C0.4284090909090909 17.068181818181817 0 15.39090909090909 0 13.626136363636363C0 11.861363636363637 0.4284090909090909 10.184090909090908 1.1778409090909092 8.718636363636364L1.1778409090909092 6.636818181818182Z" fill="#FABC05"/>
                <path d="M23.7046875 12.213802083333334C23.7046875 11.458932291666666 23.649999999999995 10.741067708333334 23.51328125 10.067317708333334H12V14.630208333333334H18.96640625C18.667708333333332 16.208932291666666 17.766119791666665 17.525520833333332 16.425 18.39765625L16.40833333333333 18.513020833333332L19.967708333333332 21.232552083333332L20.088020833333332 21.293489583333332C22.21953125 19.161458333333332 23.7046875 16.269791666666668 23.7046875 12.213802083333334Z" fill="#4285F4"/>
              </svg>
            </span>
            Sign up with Google
          </button>

          <div className="relative my-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-300 dark:border-gray-700"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-white dark:bg-gray-800 text-gray-500 dark:text-gray-400">
                Or continue with
              </span>
            </div>
          </div>

          <form className="mt-8 space-y-6" action="#" method="POST">
            <input type="hidden" name="remember" defaultValue="true" />
            <div className="rounded-md shadow-sm -space-y-px">
              <div>
                <label htmlFor="email-address" className="sr-only">
                  Email address
                </label>
                <input
                  id="email-address"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 dark:border-gray-700 placeholder-gray-500 text-gray-900 dark:text-white dark:bg-gray-700 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                  placeholder="Email address"
                />
              </div>
              <div>
                <label htmlFor="password" className="sr-only">
                  Password
                </label>
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="new-password"
                  required
                  className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 dark:border-gray-700 placeholder-gray-500 text-gray-900 dark:text-white dark:bg-gray-700 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                  placeholder="Password"
                />
              </div>
              <div>
                <label htmlFor="confirm-password" className="sr-only">
                  Confirm Password
                </label>
                <input
                  id="confirm-password"
                  name="confirm-password"
                  type="password"
                  autoComplete="new-password"
                  required
                  className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 dark:border-gray-700 placeholder-gray-500 text-gray-900 dark:text-white dark:bg-gray-700 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                  placeholder="Confirm Password"
                />
              </div>
            </div>

            <div>
              <button
                type="submit"
                className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-150 ease-in-out"
              >
                Sign Up
              </button>
            </div>
          </form>
        </div>
      </div>
    </Layout>
  );
}

export default SignUp;
