Use Effect: 
Basic Syntax:
jsx
useEffect(() => {
  // Effect code here (runs after render)
  
  return () => {
    // Cleanup code here (optional)
  }
}, [dependencies]) // Dependency array
1. useEffect without dependency array (runs after every render)
jsx
import { useEffect, useState } from 'react';

function Component() {
  const [count, setCount] = useState(0);
  const [text, setText] = useState('');

  useEffect(() => {
    console.log('Runs after EVERY render');
    console.log('Count:', count);
    console.log('Text:', text);
  });

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
      <input 
        value={text} 
        onChange={(e) => setText(e.target.value)} 
      />
    </div>
  );
}
2. useEffect with empty dependency array (runs once on mount)
jsx
import { useEffect, useState } from 'react';

function Component() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    console.log('Runs ONLY ONCE when component mounts');
    
    // Fetch data from API
    fetch('https://jsonplaceholder.typicode.com/posts/1')
      .then(response => response.json())
      .then(data => {
        setData(data);
        setLoading(false);
      });
    
    console.log('Component mounted!');
  }, []); // Empty array = runs once

  if (loading) return <div>Loading...</div>;
  return <div>{data?.title}</div>;
}
3. useEffect with dependencies (runs when dependencies change)
jsx
import { useEffect, useState } from 'react';

function Component() {
  const [count, setCount] = useState(0);
  const [name, setName] = useState('');

  useEffect(() => {
    console.log('Runs ONLY when COUNT changes');
    document.title = `Count: ${count}`;
  }, [count]); // Only runs when 'count' changes

  useEffect(() => {
    console.log('Runs ONLY when NAME changes');
    console.log(`Name changed to: ${name}`);
  }, [name]); // Only runs when 'name' changes

  useEffect(() => {
    console.log('Runs when COUNT or NAME changes');
  }, [count, name]); // Runs when any dependency changes

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
      
      <input 
        value={name} 
        onChange={(e) => setName(e.target.value)} 
        placeholder="Enter name"
      />
    </div>
  );
}
4. useEffect with Cleanup (removes event listeners, intervals, etc.)
jsx
import { useEffect, useState } from 'react';

function Component() {
  const [windowWidth, setWindowWidth] = useState(window.innerWidth);
  const [isTimerRunning, setIsTimerRunning] = useState(true);
  const [seconds, setSeconds] = useState(0);

  // Cleanup event listener
  useEffect(() => {
    console.log('Adding event listener');
    
    const handleResize = () => {
      setWindowWidth(window.innerWidth);
    };
    
    window.addEventListener('resize', handleResize);
    
    // Cleanup function (runs before component unmounts or before effect re-runs)
    return () => {
      console.log('Removing event listener');
      window.removeEventListener('resize', handleResize);
    };
  }, []); // Empty array = cleanup runs only on unmount

  // Cleanup interval
  useEffect(() => {
    if (!isTimerRunning) return;
    
    console.log('Starting timer');
    const interval = setInterval(() => {
      setSeconds(prev => prev + 1);
    }, 1000);
    
    // Cleanup runs when isTimerRunning changes or component unmounts
    return () => {
      console.log('Cleaning up timer');
      clearInterval(interval);
    };
  }, [isTimerRunning]); // Re-run when isTimerRunning changes

  return (
    <div>
      <p>Window Width: {windowWidth}px</p>
      <p>Timer: {seconds} seconds</p>
      <button onClick={() => setIsTimerRunning(!isTimerRunning)}>
        {isTimerRunning ? 'Pause' : 'Start'} Timer
      </button>
    </div>
  );
}
5. Real-world examples with your Context API:
Example A: Save theme preference to localStorage
jsx
// App.jsx
import { createContext, useState, useEffect } from "react";
import ChildA from "./assets/Components/ChildA";

const ThemeContext = createContext();

function App() {
  // Load theme from localStorage on mount
  const [theme, setTheme] = useState(() => {
    const savedTheme = localStorage.getItem('theme');
    return savedTheme || 'light';
  });

  // Save theme to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem('theme', theme);
    console.log(`Theme saved to localStorage: ${theme}`);
  }, [theme]); // Runs every time 'theme' changes

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      <ChildA />
    </ThemeContext.Provider>
  );
}

export { ThemeContext };
export default App;
Example B: Fetch user data when name changes
jsx
// ChildC.jsx
import { useContext, useEffect, useState } from "react";
import { X, Y } from "../../App";

const ChildC = () => {
  const { theme, setTheme } = useContext(X);
  const { name, setname } = useContext(Y);
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(false);

  // Fetch user data whenever name changes
  useEffect(() => {
    if (!name) return;
    
    setLoading(true);
    console.log(`Fetching data for: ${name}`);
    
    fetch(`https://api.example.com/users/${name}`)
      .then(response => response.json())
      .then(data => {
        setUserData(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching user:', error);
        setLoading(false);
      });
    
    // Optional cleanup for fetch requests
    return () => {
      console.log(`Cancelling fetch for: ${name}`);
      // In real app, you'd abort the fetch here
    };
  }, [name]); // Runs when 'name' changes

  // Log theme changes for debugging
  useEffect(() => {
    console.log(`Theme changed to: ${theme}`);
    
    // Apply theme to body class
    document.body.className = theme;
    
    return () => {
      console.log(`Cleaning up theme: ${theme}`);
      // Cleanup if needed
    };
  }, [theme]);

  return (
    <div>
      <h1>Name: {name}</h1>
      <button onClick={() => setname(name === 'shubham' ? 'rohit' : 'shubham')}>
        Change Name
      </button>

      {loading && <p>Loading user data...</p>}
      {userData && (
        <div>
          <h3>User Data:</h3>
          <pre>{JSON.stringify(userData, null, 2)}</pre>
        </div>
      )}
  
      <div style={{
        height: "100px",
        width: "100px",
        backgroundColor: theme === 'light' ? "red" : 'black'
      }}>
        <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
          Change Theme
        </button>
      </div>
    </div>
  );
}

export default ChildC;