import "./navbar.css"
import { Link } from "react-router-dom"
const Navbar = () => {
  return (
    <div>
      <ul>
        <li>
          <Link to={"/"}id='a'>Home</Link>
        </li>
        <li>
          <Link to={"/about"} id='b'>About</Link>
        </li>
        <li>
          <Link to={"/dashboard"} id='c'>Dashboard</Link>
        </li>
      </ul>
    </div>
  )
}

export default Navbar
