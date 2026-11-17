
import { useEffect, useState } from 'react'
import { apiRequest } from '../../services/api'

function Profile({ onBack, onProfileUpdated }) {
  const [profile, setProfile] = useState({
    username: '',
    email: '',
    profile_picture_url: null,
  })

  const [selectedPicture, setSelectedPicture] = useState(null)
  const [previewPicture, setPreviewPicture] = useState(null)

  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  useEffect(() => {
  if (!previewPicture) return

  return () => URL.revokeObjectURL(previewPicture)
}, [previewPicture])

  useEffect(() => {
    async function fetchProfile() {
      try {
        setLoading(true)
        setError('')

        const data = await apiRequest('/accounts/api/profile/')

        setProfile({
          username: data.username || '',
          email: data.email || '',
          profile_picture_url: data.profile_picture_url || null,
        })
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchProfile()
  }, [])

  const handleChange = (event) => {
    const { name, value } = event.target

    setProfile((previous) => ({
      ...previous,
      [name]: value,
    }))
  }

  const handlePictureChange = (event) => {
    const file = event.target.files[0]

    if (!file) return

    if (!file.type.startsWith('image/')) {
      setError('Please select a valid image file.')
      event.target.value = ''
      return
    }

    if (file.size > 5 * 1024 * 1024) {
      setError('Image size must be less than 5 MB.')
      event.target.value = ''
      return
    }

    setError('')
    setSuccess('')
    setSelectedPicture(file)
    setPreviewPicture(URL.createObjectURL(file))
  }

  const handlePictureUpload = async () => {
    if (!selectedPicture) return

    try {
      setUploading(true)
      setError('')
      setSuccess('')

      const formData = new FormData()
      formData.append('profile_picture', selectedPicture)

      const data = await apiRequest('/accounts/api/profile/', {
        method: 'PATCH',
        body: formData,
      })

      setProfile((previous) => ({
        ...previous,
        profile_picture_url: data.profile_picture_url,
      }))

      setSelectedPicture(null)
      setPreviewPicture(null)

      if (onProfileUpdated) {
        onProfileUpdated(data)
      }

      setSuccess('Profile picture uploaded successfully.')
    } catch (err) {
      setError(err.message)
    } finally {
      setUploading(false)
    }
  }

  const handleSubmit = async (event) => {
    event.preventDefault()

    try {
      setSaving(true)
      setError('')
      setSuccess('')

      const data = await apiRequest('/accounts/api/profile/', {
        method: 'PATCH',
        body: JSON.stringify({
          username: profile.username,
          email: profile.email,
        }),
      })

      setProfile((previous) => ({
        ...previous,
        username: data.username,
        email: data.email,
      }))

      if (onProfileUpdated) {
        onProfileUpdated(data)
      }

      setSuccess('Your profile was updated successfully.')
    } catch (err) {
      setError(err.message)
    } finally {
      setSaving(false)
    }
  }

  const displayedPicture =
    previewPicture || profile.profile_picture_url

  if (loading) {
    return (
      <section className="profile-page">
        <p className="profile-loading">Loading your profile...</p>
      </section>
    )
  }

  return (
    <section className="profile-page">
      <div className="profile-card">
        <div className="profile-header">
          <h2>My Profile</h2>
          <p>View and manage your account information.</p>
        </div>

        {error && (
          <div className="profile-error">
            {error}
          </div>
        )}

        {success && (
          <div className="profile-success">
            {success}
          </div>
        )}

        <div className="profile-picture-section">
          <div className="profile-picture-preview">
            {displayedPicture ? (
              <img
                src={displayedPicture}
                alt="Profile"
              />
            ) : (
              <span>
                {profile.username.charAt(0).toUpperCase() || '?'}
              </span>
            )}
          </div>

          <div className="profile-picture-controls">
            <h3>Profile Picture</h3>
            <p>Choose a picture to personalize your account.</p>

            <label
              htmlFor="profile-picture-input"
              className="profile-upload-label"
            >
              Choose Image
            </label>

            <input
              id="profile-picture-input"
              type="file"
              accept="image/*"
              onChange={handlePictureChange}
              hidden
            />

            {selectedPicture && (
              <button
                type="button"
                className="profile-save-button"
                onClick={handlePictureUpload}
                disabled={uploading}
              >
                {uploading ? 'Uploading...' : 'Upload Picture'}
              </button>
            )}

            <p className="profile-picture-hint">
              JPG, PNG or other image formats. Maximum 5 MB.
            </p>
          </div>
        </div>

        <form className="profile-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="profile-username">Username</label>
            <input
              id="profile-username"
              type="text"
              name="username"
              value={profile.username}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="profile-email">Email Address</label>
            <input
              id="profile-email"
              type="email"
              name="email"
              value={profile.email}
              onChange={handleChange}
            />
          </div>

          <div className="profile-actions">
            <button
              type="submit"
              className="profile-save-button"
              disabled={saving}
            >
              {saving ? 'Saving...' : 'Save Changes'}
            </button>

            <button
              type="button"
              className="profile-back-button"
              onClick={onBack}
            >
              Back
            </button>
          </div>
        </form>
      </div>
    </section>
  )
}

export default Profile
