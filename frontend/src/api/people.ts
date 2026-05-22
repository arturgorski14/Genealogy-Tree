import { api } from "./client";

export interface Person {
  uid: string;
  name: string;
}

export const getPeople = async (): Promise<Person[]> => {
  const res = await api.get("/people/");
  return res.data;
};

export const createPerson = async (name: string) => {
  const res = await api.post("/people/", { name });
  return res.data;
};

export const deletePerson = async (uid: string) => {
  await api.delete(`/people/${uid}`);
};