

export default function LoginPage() {
  return (
    <div className="container">
      <h3>Login:</h3>
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
        <button type="submit">
          Login
        </button>
      </form>
    </div>
  ) 
}