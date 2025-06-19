import axios from 'axios';

const BASE_URL = 'http://localhost:8000';

export async function getAllRelationships() {
  const response = await axios.get(`${BASE_URL}/relationships`);
  return response.data;
}

export async function createParentRelationship(parent_id: string, child_id: string, type: 'father' | 'mother') {
  const response = await axios.post(`${BASE_URL}/relationships/parent`, {
    parent_id,
    child_id,
    type,
  });
  return response.data;
}