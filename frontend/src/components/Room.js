import React from 'react';

function Room(props) {
  const roomCode = props.match.params.roomCode;
  return (
    <div>
      <p>HERE WE PLAY SCRABBLE!</p>
      <h4>{roomCode}</h4>
    </div>
  );
}

export default Room;