import { useContext } from "react"
import { X } from "../../App"
import {Y} from "../../App"
const ChildC = () => {

    const m=useContext(X);
    const p=useContext(Y);
    function change()
    {  
      if(m.theme==='light')
      { 
        console.log(m.theme);
        m.setTheme('dark');
       
      }
      else
      {
        m.setTheme('light');
        console.log(m.theme);
      }
    }

    function click()
    {
      if(p.name=='rahul')
      {
        p.setname('shubham');
      }
      else
      {
        p.setname('rahul');
      }
    }
  return (

    <div>
    <div id="container" style={{height:"100px",width:"100px",backgroundColor:m.theme==='light'?'red':'black'}}>
      <button onClick={change}>
        click me to change theme
      </button>
    </div>
    <div>
        <button onClick={click}>
        click to change name 
        </button>
    </div>
    </div>

     
  
  )
}

export default ChildC

// important concepts
// The Re-rendering Cycle:
// Initial Render:

// m.setname('rohit') is called during render

// This changes name from 'Rahul' to 'rohit'

// State Change Triggers Re-render:

// React detects that name state changed in App component

// React re-renders the entire App component (because state changed)

// All children (ChildA, ChildC, etc.) are re-rendered too

// During Re-render:

// The same line <h2>{m.setname('rohit')}</h2> executes AGAIN

// It calls setname('rohit') AGAIN

// But 'rohit' is already the current value

// The Problem:

// Even though the value is the same ('rohit'), React doesn't know that

// React sees a setState call and schedules another update

// This creates an infinite loop of re-renders
