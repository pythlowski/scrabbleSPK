import React from 'react';
import Square from './Square.js';

function Board({ grid, onFieldClick, lettersPoints }) {
  return (
    <div className='board-main'>
      {grid.map((row, rowIndex) => {
        return(
          <div key={200+rowIndex} className='board'>
            {row.map((element, columnIndex) => {
              return <Square 
                key={rowIndex*15+columnIndex} 
                letter={element.letter} 
                confirmed={element.confirmed}
                className={element.className}
                y={rowIndex} 
                x={columnIndex} 
                onBoard={true} 
                lettersPoints={lettersPoints}
                onFieldClick={onFieldClick} 
              />
            })}
          </div>)
      })}
    </div>
  );
}

export default Board;