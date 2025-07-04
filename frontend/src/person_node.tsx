export type Person = {
  uid: string;
  name: string;
  children?: Person[];
};

export function buildFamilyTree(people: Person[], relationships: any[]): Person[] {
  const peopleMap: Record<string, Person> = {};
  const childToParent = new Set<string>();

  // Map each person by uid
  people.forEach((person) => {
    peopleMap[person.uid] = { ...person, children: [] };
  });

  // Link children to parents
  relationships.forEach(({ parent_id, child_id }) => {
    const parent = peopleMap[parent_id];
    const child = peopleMap[child_id];
    if (parent && child) {
      parent.children?.push(child);
      childToParent.add(child.uid);
    }
  });

  // Roots are those not listed as a child
  const roots = people.filter((p) => !childToParent.has(p.uid));
  return roots.map((r) => peopleMap[r.uid]);
}


export function PersonNode({ person }: { person: Person }) {
  return (
    <li>
      {person.name} (id: {person.uid})
      {person.children && person.children.length > 0 && (
        <ul>
          {person.children.map((child) => (
            <PersonNode key={child.uid} person={child} />
          ))}
        </ul>
      )}
    </li>
  );
}
