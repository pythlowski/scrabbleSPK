import React from 'react'

export default function Square({ letter, confirmed, className, y, x, onBoard, lettersPoints, onFieldClick }) {

  // classnames: empty, filled, triple-word, triple-letter, double-word, double-letter
  var innerText = '';
  if (!letter) {
    switch(className){
      case 'triple-word': innerText = '3xW'; break;
      case 'double-word': innerText = '2xW'; break;
      case 'double-letter': innerText = '2xL'; break;
      case 'triple-letter': innerText = '3xL'; break;
    }
  }

  return (
    <div className={'square ' + (letter ? (confirmed ? 'filled' : 'filled-unconfirmed') : className)} data-y={y} data-x={x} data-board={onBoard} onClick={onFieldClick}>
      {innerText}
      {letter && <div className='letter'>{letter}</div>}
      {letter && <div className='points'>{lettersPoints[letter]}</div>}
    </div>
  )
  
}