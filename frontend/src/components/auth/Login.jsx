
import { useState } from 'react'
import { loginUser } from '../../services/auth'

function Login({ onLogin, onSwitchToRegister, onBack }) {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  })

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleChange = (event) => {
    const { name, value } = event.target

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }))
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setLoading(true)
    setError('')

    try {
      const data = await loginUser(formData)
      onLogin(data.user)
    } catch (err) {
      setError(err.message || 'Login failed. Please try again.')
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
          <h1>Welcome back</h1>
          <p>Log in to continue exploring Ethiopia.</p>
        </div>

        {error && (
          <div className="auth-error" role="alert">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="auth-form-group">
            <label htmlFor="username">Username</label>
            <input
              id="username"
              name="username"
              type="text"
              autoComplete="username"
              placeholder="Enter your username"
              value={formData.username}
              onChange={handleChange}
              required
              autoCapitalize="none"
              spellCheck={false}
            />
          </div>

          <div className="auth-form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              name="password"
              type="password"
              autoComplete="current-password"
              placeholder="Enter your password"
              value={formData.password}
              onChange={handleChange}
              required
            />
          </div>

          <button
            type="submit"
            className="auth-submit-button"
            disabled={loading}
          >
            {loading ? 'Logging in...' : 'Log in'}
          </button>
        </form>

        <p className="auth-switch">
          Don't have an account?{' '}
          <button type="button" onClick={onSwitchToRegister}>
            Create account
          </button>
        </p>
      </div>
    </section>
  )
}

export default Login
