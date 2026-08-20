import api from "../API.tsx"

export default function Signup() {

  // see login form for impl details
  const handleSubmit = async (e: SubmitEvent<HTMLFormElement>) => {
    e.preventDefault(); 

    const formEntries = new FormData(e.currentTarget); 

    const username = formEntries.get("login"); 
    const pwd_1 = formEntries.get("password"); 
    const pwd_2 = formEntries.get("password_2"); 

    if (pwd_1 !== pwd_2) {
      // tell the user something wrong;

      return;
    }

    try {
      const response = await api.post("/auth/signup", {
        'email': username, 
        'pwd': pwd_1
      });
    } catch (error: any) {

    }

  };

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