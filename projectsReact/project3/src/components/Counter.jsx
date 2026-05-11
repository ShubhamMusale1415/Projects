import { useState } from 'react'
import './Counter.css'

const Counter = () => {
    const [c ,y]=useState(10);
    // const [countvariable,setfunction]=useState(10);

  return (
    
    <div className="container">
      <p>I have clicked {c} times </p>
      <button id='btn' onClick={()=>{y(c+1)}}>click</button>
    </div>
  )
}

export default Counter

