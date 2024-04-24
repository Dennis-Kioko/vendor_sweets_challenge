import { useEffect, useState } from "react";

function VendorSweetForm({ vendorId, onAddSweet }) {
  const [sweets, setSweets] = useState([]);
  const [sweetId, setSweetId] = useState("");
  const [price, setPrice] = useState("");
  const [formErrors, setFormErrors] = useState([]);

  useEffect(() => {
    fetch("/sweets")
      .then((r) => r.json())
      .then(setSweets);
  }, []);

  function handleSubmit(e) {
    e.preventDefault();
    const formData = {
      vendor_id: vendorId,
      sweet_id: sweetId,
      price,
    };
    fetch("/vendor_sweets", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    }).then((r) => {
      if (r.ok) {
        r.json().then((sweet) => onAddSweet(sweet));
        setFormErrors([]);
      } else {
        r.json().then((err) => setFormErrors(err.errors));
      }
    });
  }

  return (
    <form onSubmit={handleSubmit}>
      <label htmlFor="sweet_id">Sweet:</label>
      <select
        id="sweet_id"
        name="sweet_id"
        value={sweetId}
        onChange={(e) => setSweetId(e.target.value)}
      >
        <option value="">Select a Sweet</option>
        {sweets.map((sweet) => (
          <option key={sweet.id} value={sweet.id}>
            {sweet.name}
          </option>
        ))}
      </select>
      <label htmlFor="strength">Price (in cents):</label>
      <input
        type="number"
        id="price"
        name="price"
        value={price}
        onChange={(e) => setPrice(parseInt(e.target.value))}
      />
      {formErrors.length > 0
        ? formErrors.map((err) => (
            <p key={err} style={{ color: "red" }}>
              {err}
            </p>
          ))
        : null}
      <button type="submit">Add Sweet</button>
    </form>
  );
}

export default VendorSweetForm;