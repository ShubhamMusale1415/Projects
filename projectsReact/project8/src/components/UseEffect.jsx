import { useEffect } from "react";
import { useState } from "react"

const UseEffect = () => {
    const [count,setCount]=useState(0);

    function click()
    {
        setCount(count+1);
    }
    useEffect(()=>
    {
      alert("value of count is "+count);
    //   console.log("value of count is ",{count});
    },[count]);

    // note: if there is no count dependency then useEffect will take place for one time only . 
    // if there is count then for every change of count useEffect will take place.
  return (
    <div>
       <h1>{count}</h1>
       <button onClick={click}>
          click
       </button>
    </div>
  )
}

export default UseEffect
