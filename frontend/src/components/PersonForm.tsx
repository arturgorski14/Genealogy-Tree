import { useState } from "react";
import { createPerson } from "../api/people";

export default function PersonForm({ onCreated }: { onCreated: () => void }) {
  const [name, setName] = useState("");

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    await createPerson(name);
    setName("");
    onCreated();
  };

  return (
    <form onSubmit={submit}>
      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Name"
      />
      <button type="submit">Add</button>
    </form>
  );
}