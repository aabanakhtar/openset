
import type { SubmitEvent } from "react"
import axios from "axios";

export default function LoginPage() {

  const handleSubmit = async (e: SubmitEvent<HTMLFormElement>) => {
    e.preventDefault(); // allows us to intercept the submission 
    
    // the data values
    const formEntries = new FormData(e.currentTarget);
    // how the oauth2passwordrequestform expects the data
    const formData = new URLSearchParams();

    const username = formEntries.get("login");
    const pwd = formEntries.get("password");

    if (!(typeof username === "string" && typeof pwd === "string")) {
      return; // what
    }

    formData.append("username", username); 
    formData.append("password", pwd); 
    console.log(`Trying to log in ${username}...`);

    try {
      // the extra header tells fastapi that we're not using json (Oauth2 form specific)
      const response = await axios.post("http://localhost:8000/auth/login", formData, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });

      console.log(response.data);
    } catch (error: any) {
      console.error(error.response?.data)
    }
    
  };


  return (
    <div className="container">
      <h3>Login:</h3>
      <form onSubmit={handleSubmit}>
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
        <p>New? Create an account</p>
        <button type="submit">
          Login
        </button>
      </form>
    </div>
  ) 
}