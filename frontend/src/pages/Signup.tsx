

export default function Signup() {
  return (
    <div className="container">
      <h3>Create Account:</h3>
      <form>
        <input 
          type="text"
          name="login"
          placeholder="Enter email"
          aria-label="Login" // screen reader stuff
          autoComplete="username" // enables browser suggestions
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Enter password"
          aria-label="Password"
          autoComplete="current-password"
          required
        />
        <input
          type="password"
          name="password_2"
          placeholder="Re-Enter password"
          aria-label="Re-Enter Password"
          autoComplete="current-password"
          required
        />
        <button type="submit">Sign Up</button>
      </form>
    </div>
  ) 
}