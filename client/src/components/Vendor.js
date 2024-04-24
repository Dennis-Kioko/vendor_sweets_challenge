import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Sweet from "./Sweet";
import VendorSweetForm from "./VendorSweetForm";

function Vendor() {
  const [{ data: vendor, error, status }, setVendor] = useState({
    data: null,
    error: null,
    status: "pending",
  });
  const { id } = useParams();

  useEffect(() => {
    fetch(`/vendors/${id}`).then((r) => {
      if (r.ok) {
        r.json().then((vendor) =>
          setVendor({ data: vendor, error: null, status: "resolved" })
        );
      } else {
        r.json().then((err) =>
          setVendor({ data: null, error: err.error, status: "rejected" })
        );
      }
    });
  }, [id]);

  function handleAddSweet(sweet) {
    setVendor({
      data: { ...vendor, vendor_sweets: [...vendor.vendor_sweets, sweet] },
      error: null,
      status: "resolved",
    });
  }

  function handleRemoveSweet(sweet) {
    debugger;
    setVendor({
      data: {
        ...vendor,
        vendor_sweets: vendor.vendor_sweets.filter((s) => s.id !== sweet.id),
      },
      error: null,
      status: "resolved",
    });
  }

  if (status === "pending") return <h1>Loading...</h1>;
  if (status === "rejected") return <h1>Error: {error.error}</h1>;

  return (
    <section>
      <h2>{vendor.name}</h2>

      <h3>Sweets:</h3>
      <ul>
        {vendor.vendor_sweets.map((sweet) => (
          <Sweet
            key={sweet.id}
            sweet={sweet}
            onRemoveSweet={handleRemoveSweet}
          />
        ))}
      </ul>

      <VendorSweetForm vendorId={vendor.id} onAddSweet={handleAddSweet} />
    </section>
  );
}

export default Vendor;