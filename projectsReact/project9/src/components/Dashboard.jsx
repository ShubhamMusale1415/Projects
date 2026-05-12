import { useNavigate } from "react-router-dom"

import { Outlet } from "react-router-dom";
const Dashboard = () => {
    const navigate=useNavigate();
function click()
{
    navigate('/about');
}
  return (
    <div>
      <h1>Its dashboard</h1>
      <button onClick={click}>
        Home page
      </button>
      <Outlet/>
    </div>
  )
}

export default Dashboard
