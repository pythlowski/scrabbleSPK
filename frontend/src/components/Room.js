import React from 'react';
import Board from './Board.js';
import Square from './Square.js';


function Room(props) {
  const roomCode = props.match.params.roomCode;
  return (
    <div className="room-main">
      <p>HERE WE PLAY SCRABBLE!</p>
      <h4>{roomCode}</h4>
      <Board />
    </div>
  );
}

export default Room;