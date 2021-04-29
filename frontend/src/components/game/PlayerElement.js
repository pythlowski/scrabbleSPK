import React from 'react';
import { TextField, Button, Grid, Typography, Paper } from "@material-ui/core";

function PlayerElement({ playerName, points }) {
  return (
    <div id="players">
      {playerName} - {points}
    </div>
  );
}

export default PlayerElement;