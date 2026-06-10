import { useEffect, useState } from "react";
import { Link } from "react-router";
import { getPeople, deletePerson } from "../api/people";
import type {Person} from "../api/people"

export default function PersonList() {
  const [people, setPeople] = useState<Person[]>([]);

  const load = async () => {
    const data = await getPeople();
    setPeople(data);
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <div>
      <h2>People</h2>
      <ul>
        {people.map((p) => (
          <li key={p.uid}>
            <Link to={`/person/${p.uid}`}>{p.name}</Link>
            <button onClick={async () => {
              await deletePerson(p.uid);
              load();
            }}>
              ❌
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}