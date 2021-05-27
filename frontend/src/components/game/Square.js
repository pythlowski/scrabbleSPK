import React, {useState} from 'react'

export default function Square({ letter, confirmed, toExchange, className, y, x, onBoard, lettersPoints, onFieldClick }) {

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
    <div className={'square ' + (letter ? (confirmed ? 'filled ' : 'filled-unconfirmed ') : className) + (toExchange ? 'selected-to-exchange' : '')} data-y={y} data-x={x} data-board={onBoard} onClick={onFieldClick}>
      {innerText}
      {letter && <div className='letter'>{letter[0] == 'b' ? letter[1] : letter}</div>}
      {letter && letter != ' ' && <div className='points'>{lettersPoints[letter]}</div>}
    </div>
  )
  
}