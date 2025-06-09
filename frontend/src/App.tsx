import { useEffect, useState } from 'react';
import { getAllPeople, createPerson } from './api/people';

function App() {
  const [people, setPeople] = useState([]);
  const [newName, setNewName] = useState('');

  useEffect(() => {
    getAllPeople().then(setPeople).catch(console.error);
  }, []);

  const handleCreate = async () => {
    const newPerson = await createPerson(newName);
    setPeople([...people, newPerson]);
    setNewName('');
  };

  return (
    <div>
      <h1>People</h1>
      <ul>
        {people.map((p) => (
          <li key={p.uid}>{p.name}</li>
        ))}
      </ul>
      <input
        type="text"
        value={newName}
        onChange={(e) => setNewName(e.target.value)}
        placeholder="New name"
      />
      <button onClick={handleCreate}>Add Person</button>
    </div>
  );
}

export default App;
