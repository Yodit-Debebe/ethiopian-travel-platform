
import { useState } from 'react'
import { registerUser } from '../../services/auth'

function Register({ onSwitchToLogin, onBack }) {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
  })

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const handleChange = (event) => {
    const { name, value } = event.target

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }))
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError('')
    setSuccess('')

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match.')
      return
    }

    if (formData.password.length < 8) {
      setError('Password must contain at least 8 characters.')
      return
    }

    setLoading(true)

    try {
      await registerUser({
        username: formData.username,
        email: formData.email,
        password: formData.password,
      })

      setSuccess('Registration successful! You can now log in.')
      setFormData({
        username: '',
        email: '',
        password: '',
        confirmPassword: '',
      })
    } catch (err) {
      setError(err.message || 'Registration failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="auth-section">
      <div className="auth-card">
        <button
          type="button"
          className="auth-back-button"
          onClick={onBack}
        >
          ← Back to EthioExplore
        </button>

        <div className="auth-heading">
          <span className="brand-mark">E</span>
          <h1>Create your account</h1>
          <p>Join EthioExplore and discover Ethiopia.</p>
        </div>

        {error && <div className="auth-error" role="alert">{error}</div>}

        {success && <div className="auth-success" role="status">{success}</div>}

        <form onSubmit={handleSubmit}>
          <div className="auth-form-group">
            <label htmlFor="register-username">Username</label>
            <input
              id="register-username"
              name="username"
              type="text"
              placeholder="Choose a username"
              value={formData.username}
              onChange={handleChange}
              required
              spellCheck={false}
              autoCapitalize="none"
              autoComplete="username"
            />
          </div>

          <div className="auth-form-group">
            <label htmlFor="register-email">Email address</label>
            <input
              id="register-email"
              name="email"
              type="email"
              placeholder="Enter your email"
              value={formData.email}
              onChange={handleChange}
              required
              autoComplete="email"
            />
          </div>

          <div className="auth-form-group">
            <label htmlFor="register-password">Password</label>
            <input
              id="register-password"
              name="password"
              type="password"
              placeholder="Create a password"
              value={formData.password}
              onChange={handleChange}
              minLength={8}
              required
              autoComplete="new-password"
            />
          </div>

          <div className="auth-form-group">
            <label htmlFor="confirm-password">Confirm password</label>
            <input
              id="confirm-password"
              name="confirmPassword"
              type="password"
              placeholder="Confirm your password"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
              autoComplete="new-password"
            />
          </div>

          <button
            type="submit"
            className="auth-submit-button"
            disabled={loading}
          >
            {loading ? 'Creating account...' : 'Create account'}
          </button>
        </form>

        <p className="auth-switch">
          Already have an account?{' '}
          <button type="button" onClick={onSwitchToLogin}>
            Log in
          </button>
        </p>
      </div>
    </section>
  )
}

export default Register
