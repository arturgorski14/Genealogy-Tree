import axios from 'axios';

const BASE_URL = 'http://localhost:8000';

export async function getAllPeople() {
  const response = await axios.get(`${BASE_URL}/people`);
  return response.data;
}

export async function getPerson(id: string) {
  const response = await axios.get(`${BASE_URL}/people/${id}`);
  return response.data;
}

export async function createPerson(name: string) {
  const response = await axios.post(`${BASE_URL}/people`, {
    name,
  });
  return response.data;
}

export async function deletePerson(personId: string) {
  const response = await axios.delete(`${BASE_URL}/people/${personId}`);
  return response.data;
}