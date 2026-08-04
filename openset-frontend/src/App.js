import React, {useEffect, useState} from 'react';
import axios from 'axios'; 

export default function App() {
  const [appHealth, setAppHealth] = useState(""); 
  const [loaded, setLoaded] = useState(false); 

  useEffect(() => {
    axios.get("http://localhost:8000/health")
    .then(res => {
      const health = res.data.status; 
      setAppHealth(health); 
      setLoaded(true);
    })
    .catch(err => {
      setLoaded(true); 
      setAppHealth("bad health");
    })
  }, []);

  let content = <p>"Waiting for valid response...."</p>; 
  if (loaded) {
    content = <p>{appHealth}</p>
  }

  return (
    <div>
      <h1>Welcome to Openset!</h1>
      <p>App Health: </p>
      {content}
    </div>
  );
}