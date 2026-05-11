

function App() {
 function click()
 {
  alert("Thanks , you clikced me ...");
 }
 function onchange(e)
 {
  console.log("new value",e.target.value);
 }
 function onsubmit(e)
 {
  e.preventDefault();
  alert("form submit kar raha hu....");
 }
  return (
  
    <div>
     

      <form onSubmit={onsubmit}>
        <input type="text" onChange={onchange} />
      <button type="submit">submit</button>
      </form>
       <button onClick={click}>
        <h1>click</h1>
      </button>
    </div>
  
  )
}

export default App
