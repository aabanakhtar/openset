
import type { SubmitEvent } from "react"
import axios from "axios";
import api from "../API"
import { Link, useNavigate } from "react-router-dom";

export default function LoginPage() {
  // must be declared outside
  const navigate = useNavigate();

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
      const response = await api.post("/auth/login", formData, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });

      // store it
      sessionStorage.setItem("access_token", response.data.access_token);
      // go to dashboard
      navigate("/dash")
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
        <p>New? <Link to="/signup">Create an account</Link></p>
        <button type="submit">
          Login
        </button>
      </form>
    </div>
  ) 
}