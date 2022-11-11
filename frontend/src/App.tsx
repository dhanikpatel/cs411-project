import React, { useState, useEffect } from "react";
import './App.css'

function App() {
  const [data, setData] = useState({});

  useEffect(() => {
    
    fetch('/me/playlists')
      .then((response) => {
        console.log(response)
        if (response.ok) {
          return response.json();
        }
      })
      .then((data) => {
        console.log("Hello");
        console.log(data);
        setData({
          // do not know the shape of data
        })
      })
      
  }, [])

  return (
    <div className="App">
      <header className="App-header">
      <h2>Hi Name!</h2>
      <hr></hr>
      <p>One of your playlists is called: ... .</p>
      </header>
    </div>
    
  
  )
}

export default App
