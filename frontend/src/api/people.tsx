import axios from 'axios';

export async function getAllPeople() {
  const response = await axios.get('http://localhost:8010/people'); // sufficient for quick test
  return response.data; // axios unwraps JSON automatically
}
