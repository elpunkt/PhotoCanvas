import axios from 'axios'
import {apiUrl} from '@/env'

export const apiClient = axios.create({
  // baseURL: 'https://my-json-server.typicode.com/bipinstha7/vue-design-pattern',
  baseURL: apiUrl,
  timeout: 5000 // throw error if API call takes longer than 10 seconds
});

function authHeaders(token) {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
}

export const Api = {
  async logInGetToken(username, password) {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);
    return apiClient.post('/login/access-token', params);
  },
  async getMe(token) {
    return apiClient.get('/users/me', authHeaders(token))
  },
  async updateMe(token, payload) {
    return apiClient.put('/users/me', payload, authHeaders(token))
  },
  async updatePasswordMe(token, payload) {
    return apiClient.put('/users/me/password', payload, authHeaders(token))
  },
  async signUp(payload) {
    return apiClient.post('/users/signup', payload)
  },
  async getUsers(token) {
    return apiClient.get('/users', authHeaders(token))
  },
  async getUser(token, id) {
    return apiClient.get(`/users/${id}`, authHeaders(token))
  },
  async createUser(token, payload) {
    return apiClient.post('/users', payload, authHeaders(token))
  },
  async updateUser(token, id, payload) {
    return apiClient.put(`/users/${id}`, payload, authHeaders(token))
  },
  async deleteUser(token, id) {
    return apiClient.delete(`/users/${id}`, authHeaders(token))
  },
  async passwordRecovery(username) {
    return apiClient.post(`/password-recovery/${username}`)
  },
  async resetPassword(payload) {
    return apiClient.post('/reset-password', payload)
  },
  async uploadPhoto(file, title) {
    let form_data = new FormData();
    form_data.append('photo', file, file.name);
    form_data.append('title', title)
    return apiClient.post('/upload', form_data, {headers: {'Content-Type': 'multipart/form-data'}} );
  },
  async getAllPhotos(token) {
    return apiClient.get('/photos', authHeaders(token))
  },
  async deletePhoto(token, id) {
    return apiClient.delete('/photos/' + id, authHeaders(token))
  },
  async rotatePhoto(token, id) {
    return apiClient.get('/photos/' + id + '/rotate', authHeaders(token))
  }
}
