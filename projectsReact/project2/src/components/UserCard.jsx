

import "./UserCard.css"
const UserCard = (props) => {
  return (
    <div className='user-container'>
      <p id='user-name'>{props.name}</p>
      <p>{props.movie.x}</p>
      <p>{props.movie.y}</p>
      <img id='user-img' src={props.imgi} alt="shubh" />
      <p id='user-desc'>
         {props.desc}
      </p>
    </div>
  )
}

export default UserCard
