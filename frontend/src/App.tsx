import PersonList from "./components/PersonList";
import PersonForm from "./components/PersonForm";
import { useRef } from "react";

export default function App() {
  const listRef = useRef<any>();

  return (
    <div style={{ padding: 20 }}>
      <h1>Family Tree - list</h1>
      <PersonForm onCreated={() => listRef.current?.load?.()} />
      <PersonList ref={listRef} />
    </div>
  );
}