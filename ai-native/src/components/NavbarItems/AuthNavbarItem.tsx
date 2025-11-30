import React from 'react';
import NavbarItem from '@theme/NavbarItem';
import { useHistory } from '@docusaurus/router';

export default function AuthNavbarItem(props) {
  const history = useHistory();

  const handleSignInClick = () => {
    history.push('/login');
  };

  return (
    <NavbarItem
      {...props}
      label="Sign In"
      onClick={handleSignInClick}
      to="/login" // This 'to' prop is used for styling/active state by Docusaurus, even if we handle navigation manually.
    />
  );
}
