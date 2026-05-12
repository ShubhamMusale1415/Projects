import { createBrowserRouter,RouterProvider }  from "react-router-dom";
import Home from "./components/Home"
import Dashboard from "./components/Dashboard"
import About from "./components/About"
import Navbar  from "./components/Navbar";
import Done from "./components/Done";
import Dtwo from "./components/Dtwo";
import Error from "./components/Error";
const router=createBrowserRouter([
    {
      path:"/",
      element:
      <div>
      <Navbar/>
      <Home/>
      </div>
    },
    {
       path:"/about",
      element: <div>
        <Navbar/>
        <About/>
      </div>
    },
    {
       path:"/dashboard",
      element:  <div>
        <Navbar/>
        <Dashboard/>
      </div>,
      children:
      [
        {
           path:"done",
           element:<Done/>
        },
        {
           path:"dtwo",
           element:<Dtwo/>
        }

      ]
    },
    {
       path:"*",
      element: <div>
        <Error/>
      </div>
    },
   ]);


function App() {
  
  return (
     <RouterProvider router={router}/>
  )
}

export default App
