import React, { useState } from 'react';
import { TextField, Button, Grid, Typography } from "@material-ui/core";
import { useHistory } from "react-router-dom";

function NicknamePage(props) {

  const [nickname, setNickname] = useState('');
  const history = useHistory();

  function onTextFieldChange(e) {
    setNickname(e.target.value);
  }

  function generateRandomNickname(e) {
    console.log(nickname);
    let nick = "gracz";
    for (let i=0; i<5; i++) {
      nick += Math.floor(Math.random()*9)
    }
    setNickname(nick);
  }

  function onNicknameConfirm(e) {
    if (nickname){
      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nickname: nickname }),
      };
      fetch("/api/nickname-session/", requestOptions)
        .then(response => response.json())
        .then(_ => history.push("/list", { from: "NicknamePage" }));
    } else {
      alert('Podaj nickname.');
    }
  }

  return (
    <Grid container spacing={1}>
      <Grid item xs={12} align="center">
        <Typography component="h3" variant="h3">
          Witaj w ScrabbleSPK!
        </Typography>
      </Grid>

      <Grid item xs={12} align="center">
        <Typography component="h4" variant="h4">
          Wpisz nickname lub wygeneruj:
        </Typography>
      </Grid>

      <Grid item xs={12} align="center">
        <TextField
          value={nickname}
          label="nickname"
          required={true}
          onChange={onTextFieldChange}
        />
      </Grid>

      <Grid item xs={12} align="center">
        <Button 
          color="primary"
          variant="contained"
          onClick={generateRandomNickname}
        >
          Wygeneruj losowy
        </Button>
      </Grid>

      <Grid item xs={12} align="center">
        <Button 
          color="secondary"
          variant="contained"
          onClick={onNicknameConfirm}
        >
          Potwierdź
          </Button>
      </Grid>
    </Grid>
  );
}

export default NicknamePage;