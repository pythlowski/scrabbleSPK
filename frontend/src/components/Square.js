import React, {useState} from 'react'

// Represents a grid square with a color

export default function Square(props) {

  //console.log(props.x, props.y);

  

  function getSelected(e){
    //setLetter("X");
    setSelection("Yes");
    props.passTheCoords(props.x, props.y)
  }

  function getSelectedLetter(e){
    setLetter("X");
    setSelection("Yes");
  }

  var str1 = "rectangle-"
  var str2 = props.type
  var res = str1.concat(str2)

  const [letter, setLetter] = useState("")
  const [isEditable, ss] = useState("")
  const [isSelected, setSelection] = useState("No")


  if (letter != "Null" && props.type == "normal"){
  return (
  <div className={res} onClick ={getSelected}>
    <input type='text' size="1" onChange={e => {setLetter(e.target.value) ;ss("disabled")}}  maxLength="1" disabled={isEditable}/>
    {letter}
    </div>
    
  )
  }
  else if (letter != "Null" && props.type == "myLetters")
  {
    return(
    <div className={res} onClick ={getSelectedLetter}>
    <p>{letter}</p>
    </div>
    )
  }
  else { //tutaj sytuacja kiedy przekazujemy pusty Square
    return (
      <div className={res} onClick ={getSelected}>
        <input type='text' size="1" onChange={e => {setLetter(e.target.value) ;ss("disabled")}}  maxLength="1" disabled={isEditable}/>
        </div>
    )
  }
  
}