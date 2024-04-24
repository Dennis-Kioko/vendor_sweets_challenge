import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

function Home() {
  const [vendors, setVendors] = useState([]);

  useEffect(() => {
    fetch("/vendors")
      .then((r) => r.json())
      .then(setVendors);
  }, []);

  return (
    <section>
      <h2>All Vendors</h2>
      <ul>
        {vendors.map((vendor) => (
          <li key={vendor.id}>
            <Link to={`/vendors/${vendor.id}`}>{vendor.name}</Link>
          </li>
        ))}
      </ul>
    </section>
  );
}

export default Home;