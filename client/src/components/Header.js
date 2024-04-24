import { Link } from "react-router-dom";

function Header() {
  return (
    <header>
      <Link to="/">
        <h1>Vendor Sweets</h1>
      </Link>
    </header>
  );
}

export default Header;