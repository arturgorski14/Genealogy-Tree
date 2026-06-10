import { BrowserRouter, Routes, Route } from "react-router";
import PersonList from "./components/PersonList";
import PersonDetails from "./components/PersonDetails";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<PersonList />} />
        <Route path="/person/:uid" element={<PersonDetails />} />
      </Routes>
    </BrowserRouter>
  );
}