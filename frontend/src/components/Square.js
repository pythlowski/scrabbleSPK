import React, {useState} from 'react'

// Represents a grid square with a color

export default function Square(props) {

  var str1 = "rectangle-"
  var str2 = props.type
  var res = str1.concat(str2)
  var text = 'text'
  var hidden = 'hidden'
  const [letter, setLetter] = useState('')
  const [isEditable, ss] = useState("")

  return (
  <div className={res} >
    <input type='text' size="1" onChange={e => {setLetter(e.target.value) ;ss("disabled")}}  maxlength="1" disabled={isEditable}/>
    {letter}
    {isEditable.toString()}
    </div>
    
  )
  
}