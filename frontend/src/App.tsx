import "@picocss/pico"
import "./App.css"

import { Routes, Route, Link } from "react-router-dom";
import { useState } from "react";

import Login from "./pages/Login"
import { Home } from "./pages/Home";
import Signup from "./pages/Signup";

function NavHeader() {
  return (
    <div className="container">
      <nav>
        <ul>
          <li><Link to="/"><h2><img className="logo" src="public/logo.png" /></h2></Link></li>
        </ul>
        <ul>
          <li><Link to="/">Recommender Login</Link></li>
          <li><Link to="/signup">Sign Up</Link></li> 
          <li><Link to="/login">Log in</Link></li>
        </ul>
      </nav>
    </div>
  );
}

function App() {
  const [authToken, setAuthToken] = useState("");

  return (
    <div>
      <NavHeader/>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/signup" element={<Signup />}/>
        <Route path="/login" element={<Login/>} />
      </Routes>
    </div>
  );
}

export default App;
