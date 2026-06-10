import { useEffect, useState } from "react";
import { useParams } from "react-router";
import { api } from "../api/client";

export default function PersonDetails() {
  const { uid } = useParams();
  const [person, setPerson] = useState<any>(null);

  useEffect(() => {
    const load = async () => {
      const res = await api.get(`/people/${uid}`);
      setPerson(res.data);
    };

    load();
  }, [uid]);

  if (!person) return <div>Loading...</div>;

  return (
    <div>
      <h2>{person.name}</h2>
      <p>ID: {person.uid}</p>
    </div>
  );
}