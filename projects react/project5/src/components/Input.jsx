
const Input = (props) => {
    function change(e)
    {
    props.setname(e.target.value);
       }
  return (
    <div>
      <input type="text" onChange={change}/>
      <p>You have entered:{props.name}</p>
    </div>
  )
}
export default Input
