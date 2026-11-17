
import { apiRequest } from './api'

export async function registerUser(userData) {
  return apiRequest('/accounts/api/register/', {
    method: 'POST',
    body: JSON.stringify(userData),
  })
}

export async function loginUser(credentials) {
  const data = await apiRequest('/accounts/api/login/', {
    method: 'POST',
    body: JSON.stringify(credentials),
  })

  localStorage.setItem('authToken', data.token)
  localStorage.setItem('currentUser', JSON.stringify(data.user))

  return data
}

export async function logoutUser() {
  try {
    await apiRequest('/accounts/api/logout/', {
      method: 'POST',
    })
  } finally {
    localStorage.removeItem('authToken')
    localStorage.removeItem('currentUser')
  }
}

export function getCurrentUser() {
  try {
    const user = localStorage.getItem('currentUser')

    return user ? JSON.parse(user) : null
  } catch (error) {
    console.error('Failed to restore current user:', error)

    localStorage.removeItem('currentUser')
    localStorage.removeItem('authToken')

    return null
  }
}

export function isAuthenticated() {
  return Boolean(localStorage.getItem('authToken'))
}
