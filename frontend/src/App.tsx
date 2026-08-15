import "@picocss/pico"
import "./App.css"

import { Routes, Route, Link } from "react-router-dom";

import Login from "./pages/Login"
import { Home } from "./pages/Home";

function NavHeader() {
  return (
    <div className="container">
      <nav>
        <ul>
          <li><Link to="/"><h2><strong>Referly</strong></h2></Link></li>
        </ul>
        <ul>
          <li><Link to="/" role="button">Recommender Login</Link></li>
          <li><Link to="/login" role="button">Log in</Link></li>
        </ul>
      </nav>
    </div>
  );
}

function App() {
  return (
    <div>
      <NavHeader/>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login/>} />
      </Routes>
    </div>
  );
}

export default App;
