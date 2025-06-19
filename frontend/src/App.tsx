import { useEffect, useState } from 'react';
import { getAllPeople, createPerson } from './api/people';
import { getAllRelationships } from './api/relationships';
import { PersonNode, buildFamilyTree } from './person_node';
import { createParentRelationship } from './api/relationships';

function App() {
  const [people, setPeople] = useState([]);
  const [newName, setNewName] = useState('');
  const [relationships, setRelationships] = useState([]);
  const [tree, setTree] = useState([]);
  const [parentId, setParentId] = useState('');
  const [childId, setChildId] = useState('');
  const [parentType, setParentType] = useState<'father' | 'mother'>('father');

  useEffect(() => {
    async function fetchData() {
      try {
        const [peopleData, relationshipData] = await Promise.all([
          getAllPeople(),
          getAllRelationships(),
        ]);
        setPeople(peopleData);
        setRelationships(relationshipData);
        setTree(buildFamilyTree(peopleData, relationshipData));
      } catch (err) {
        console.error(err);
      }
    }
    fetchData();
  }, []);

  const handleCreate = async () => {
    const newPerson = await createPerson(newName);
    const updatedPeople = [...people, newPerson];
    setPeople(updatedPeople);
    setNewName('');
    setTree(buildFamilyTree(updatedPeople, relationships)); // update tree
  };

  const handleCreateRelationship = async () => {
      try {
        await createParentRelationship(parentId, childId, parentType);
        const updatedRelationships = await getAllRelationships();
        setRelationships(updatedRelationships);
        setTree(buildFamilyTree(people, updatedRelationships)); // update tree
        setParentId('');
        setChildId('');
      } catch (error) {
        console.error('Failed to create relationship', error);
      }
};

  return (
    <div>
      <div>
        <h1>People</h1>
        <ul>
          {people.map((p) => (
            <li key={p.uid}>
              {p.name} id: {p.uid}
            </li>
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

      <div>
        <h1>Family Tree</h1>
        <ul>
          {tree.map((rootPerson) => (
            <PersonNode key={rootPerson.uid} person={rootPerson} />
          ))}
        </ul>
      </div>

      <div>
          <h2>Create Parent Relationship</h2>
          <select value={parentId} onChange={(e) => setParentId(e.target.value)}>
            <option value="">Select Parent</option>
            {people.map((p) => (
              <option key={p.uid} value={p.uid}>
                {p.name} (id: {p.uid})
              </option>
            ))}
          </select>

          <select value={childId} onChange={(e) => setChildId(e.target.value)}>
            <option value="">Select Child</option>
            {people.map((p) => (
              <option key={p.uid} value={p.uid}>
                {p.name} (id: {p.uid})
              </option>
            ))}
          </select>

          <select value={parentType} onChange={(e) => setParentType(e.target.value as 'father' | 'mother')}>
            <option value="father">Father</option>
            <option value="mother">Mother</option>
          </select>

          <button onClick={handleCreateRelationship}>Add Relationship</button>
        </div>
    </div>
  );
}

export default App;
