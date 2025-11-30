import React, {useEffect, useState} from 'react';
import * as ReactDOMClient from 'react-dom/client';
import Link from '@docusaurus/Link';

function AuthWidget(): JSX.Element {
  const [signedIn, setSignedIn] = useState<boolean>(() => {
    try {
      return Boolean(localStorage.getItem('authToken'));
    } catch (e) {
      return false;
    }
  });

  useEffect(() => {
    function onStorage() {
      try {
        setSignedIn(Boolean(localStorage.getItem('authToken')));
      } catch (e) {
        setSignedIn(false);
      }
    }
    window.addEventListener('storage', onStorage);
    return () => window.removeEventListener('storage', onStorage);
  }, []);

  const signOut = (e: React.MouseEvent) => {
    e.preventDefault();
    try {
      localStorage.removeItem('authToken');
      sessionStorage.removeItem('authToken');
    } catch (err) {
      // ignore
    }
    setSignedIn(false);
    // navigate to our logout page for UX
    window.location.href = '/logout';
  };

  if (signedIn) {
    return (
      <div className="navbar__items">
        <a className="navbar__link" href="/logout" onClick={signOut}>
          Sign Out
        </a>
      </div>
    );
  }

  return (
    <div className="navbar__items">
      <Link className="navbar__link" to="/login">
        Sign In
      </Link>
    </div>
  );
}

// Mount the widget into the DOM placeholder
export default function (): void {
  if (typeof document === 'undefined') return;
  const mountPoint = document.getElementById('auth-root');
  if (!mountPoint) return;

  try {
    const root = ReactDOMClient.createRoot(mountPoint);
    root.render(<AuthWidget />);
  } catch (e) {
    // Fallback for older React renderers
    // eslint-disable-next-line @typescript-eslint/no-var-requires
    const ReactDOM = require('react-dom');
    ReactDOM.render(React.createElement(AuthWidget), mountPoint);
  }
}
