import React from 'react';
import NavbarItem from '@theme/NavbarItem';
import { useHistory } from '@docusaurus/router';

export default function SignOutNavbarItem(props) {
  const history = useHistory();

  const handleSignOutClick = () => {
    // Here you would typically clear authentication tokens, session data, etc.
    // For this example, we'll just redirect to a /logout page.
    history.push('/logout');
  };

  return (
    <NavbarItem
      {...props}
      label="Sign Out"
      onClick={handleSignOutClick}
      to="/logout" // This 'to' prop is used for styling/active state by Docusaurus.
    />
  );
}
