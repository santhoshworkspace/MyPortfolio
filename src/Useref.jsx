import React, { useState } from 'react'

const Useref = () => {
    const [without,setwithout]=useState()
    const inputref=Useref()
    const change =()=>{
       console.log(inputref.current.value);  
    }
   
  return (
    <div>
      <input type="text" onChange={(e)=>setwithout(e.target.value)}/>
      <button onClick={change}></button>
<p>{without}</p>
    </div>
  )
}

export default Useref 
