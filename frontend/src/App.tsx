import { useEffect, useState } from 'react';
import { getAllPeople, createPerson, deletePerson } from './api/people';
import { getAllRelationships } from './api/relationships';
import { PersonNode, buildFamilyTree } from './person_node';
import { createParentRelationship, deleteParentRelationship } from './api/relationships';

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
        await createParentRelationship(parentId, childId, parentType);  // TODO: need better response from backend, and then just add to the list
        const updatedRelationships = await getAllRelationships();  // TODO: then this call becomes redundant (and that's perfect)
        setRelationships(updatedRelationships);
        setTree(buildFamilyTree(people, updatedRelationships)); // update tree
        setParentId('');
        setChildId('');
      } catch (error) {
        console.error('Failed to create relationship', error);
      }
  };

  const handleDeletePerson = async (uid: string) => {
  try {
    await deletePerson(uid);
    const updatedPeople = people.filter((p) => p.uid !== uid);
    const updatedRelationships = relationships.filter(
      (r) => r.parent_id !== uid && r.child_id !== uid
    );
    setPeople(updatedPeople);
    setRelationships(updatedRelationships);
    setTree(buildFamilyTree(updatedPeople, updatedRelationships));
  } catch (error) {
    console.error('Failed to delete person', error);
  }
};

const handleDeleteRelationship = async (parentId: string, childId: string) => {
  try {
    await deleteParentRelationship(parentId, childId);
    const updatedRelationships = relationships.filter(
      (r) => !(r.parent_id === parentId && r.child_id === childId)
    );
    setRelationships(updatedRelationships);
    setTree(buildFamilyTree(people, updatedRelationships));
  } catch (error) {
    console.error('Failed to delete relationship', error);
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
              <button onClick={() => handleDeletePerson(p.uid)} style={{ marginLeft: '8px', color: 'red' }}>
                Delete
              </button>
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

      <div>
          <h2>Relationships</h2>
          <ul>
            {relationships.map((r) => (
              <li key={`${r.parent_id}-${r.child_id}`}>
                parent: {r.parent_id} → child: {r.child_id} ({r.type})
                <button
                  onClick={() => handleDeleteRelationship(r.parent_id, r.child_id)}
                  style={{ marginLeft: '8px', color: 'red' }}
                >
                  Delete
                </button>
              </li>
            ))}
          </ul>
        </div>
    </div>
  );
}

export default App;