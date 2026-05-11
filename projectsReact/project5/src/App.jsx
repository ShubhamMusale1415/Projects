
import { useState } from 'react'
import './App.css'
import Input from './components/Input.jsx'
import Login from "./components/Login.jsx"
import Logout from './components/Logout.jsx'
function App() {
   const[islogged]=useState(true);
    // const[islogged,setlogged]=useState(true);
    // as there is not cumpulsory to use setlogged respectively.
   const [name,setname]=useState('');
   
      if(!islogged)
        {
          return (
            <div>
                <Input name={name} setname={setname}/>
            <Input name={name} setname={setname}/>
            <Login/>
            </div>
          
          )
        }
        else
        {
          return(
           <div>
              <Input name={name} setname={setname}/>
            <Input name={name} setname={setname}/>
            <Logout/>
           </div>
          )
        }
}

export default App
