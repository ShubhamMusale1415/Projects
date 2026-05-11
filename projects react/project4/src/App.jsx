
import { useState } from 'react';
import './App.css'
import Children  from './components/Children.jsx';
import Functional  from './components/Functional.jsx';
function App() {
   
  const [count,setcount]=useState(10);
  function change()
  {
    setcount(count+1);
  }
  return (
    <>
      <Children>
        <p>Hii Shubham</p>
        <h1>its krish</h1>
      </Children>
      <Functional x={change} count={count}/>
    </>
  )
}

export default App
