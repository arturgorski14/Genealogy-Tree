import { useEffect, useState } from 'react'
import { getAllPeople } from './api/people';
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)
  const [people, setPeople] = useState([]);

  useEffect(() => {
    getAllPeople()
      .then(setPeople)
      .catch((err) => console.error('Failed to load people:', err));
  }, []);

  return (
    <div>
      <h1>People</h1>
      <ul>
        {people.map((p) => (
          <li key={p.uid}>{p.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default App
