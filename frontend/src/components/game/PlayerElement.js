import React from 'react';
import { TextField, Button, Grid, Typography, Paper } from "@material-ui/core";

function PlayerElement({ playerName, points, theirTurn, isHost }) {
  return (
    <div className={theirTurn ? 'player-with-turn' : 'player'}>
      {isHost && '*'}{playerName} - {points}
    </div>
  );
}

export default PlayerElement;