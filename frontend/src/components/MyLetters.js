import React from 'react';
import Square from './Square.js';

export default function MyLetters(props) {

    const lettersTable = ["A", "B", "C", "D" ,"E", "F", "G"]
    const lettersGrid = []

    for (let i = 0; i < lettersTable.length; i ++) {
        lettersGrid.push(<Square type= "myLetters" id={i} key={`${i}`} letter={lettersTable[i].toString()} />)
    }

    return (
        <div className="lettersList">
          {lettersGrid}
        </div>
      );
  
}