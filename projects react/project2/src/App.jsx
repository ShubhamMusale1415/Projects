
import './App.css'
import UserCard from './components/UserCard'

import one from "./assets/react.svg"
function App() {
  


  return (
    <>
      <div className='container'>
       <UserCard name='shubham' desc='desc1' imgi={one} movie={{x:'shubham',y:'om'}} />
       <UserCard name='om' desc='desc2' imgi={one} movie={{x:'shubham',y:'om'}}/>
       <UserCard name='shree' desc='desc3' imgi={one} movie={{x:'shubham',y:'om'}}/>
      </div>
    </>
  )
}

export default App
