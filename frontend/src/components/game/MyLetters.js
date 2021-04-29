import React from 'react';
import Square from './Square.js';

export default function MyLetters({ letters, lettersPoints, onFieldClick }) {
  return (
      <div id="my-letters">
        {letters.map((letter, index) => {
          return <Square 
            key={1000+index}
            y={0} 
            x={index} 
            onBoard={false} 
            letter={letter.letter} 
            confirmed={true}
            className={letter.letter ? 'filled' : 'empty-in-hand'}
            lettersPoints={lettersPoints}
            onFieldClick={onFieldClick}
            />
        })}
      </div>
    );
  
}