import { useState } from "react";
function ExampleForm() {
  const [value, setValue] = useState("");

  const handleChange = (event: { target: { value: string } }) => {
    setValue(event.target.value.toUpperCase());
  };

  return (
    <form>
      <input type="text" value={value} onChange={handleChange} />
      <pre>{value}</pre>
    </form>
  );
}

export default ExampleForm;
