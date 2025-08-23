import { useEffect, useState } from 'react';
import { getAllPeople, createPerson, deletePerson } from './api/people';
import { getAllRelationships } from './api/relationships';
import { PersonNode, buildFamilyTree } from './person_node';
import { createParentRelationship, deleteParentRelationship } from './api/relationships';

function App() {
    return (
        <div>
        <h1>Family Tree</h1>
        <h3>New version incoming :)</h3>
      </div>
    )
};


export default App;