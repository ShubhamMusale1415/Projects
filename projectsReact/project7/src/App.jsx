import { createContext } from "react"
import ChildA from "./assets/Components/ChildA"

import { useState } from "react";
// first context is created respectively.
const X=createContext();
const Y=createContext();

function App() {

const [name, setname]=useState('rahul');
const [theme,setTheme]=useState('light');

  return (
    <>
      <X.Provider value={{theme,setTheme}}>
         <Y.Provider value={{name,setname}}>
         <ChildA/ >
      </Y.Provider>
      
      </X.Provider>
     
      <h1>name:{name}</h1>
    </>
  )
}

// note :
//  <X.Provider value={{theme,setTheme}}>
//         <ChildA/ >
//       </X.Provider>
//       <Y.Provider value={{name,setname}}>
//       <ChildA/> 
//       </Y.Provider>  this is write way to use two hooks to same component 

// another wrong method:
// <X.Provider value={{theme,setTheme,name,setname}}>
//         <ChildA/ >
//       </X.Provider>
 // as above also two hooks parameters are passed in one only its wrong.
export {X,Y};// export {X},{Y} it is not the correct way to 

export default App;