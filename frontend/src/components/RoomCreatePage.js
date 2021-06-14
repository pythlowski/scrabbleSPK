import React, { useState } from 'react';
import { TextField, Button, Grid, Typography, FormControl, FormHelperText, RadioGroup, FormControlLabel, Radio } from "@material-ui/core";
import { useHistory } from "react-router-dom";

function RoomCreatePage(props) {
  const [isPublic, setPublic] = useState(true);
  const [limit, setLimit] = useState(4);
  const history = useHistory();

  function handleRoomPrivacy(e){
    setPublic(e.target.value === "true" ? true : false);
  }

  function onPlayersLimitChange(e){
    setLimit(e.target.value);
  }

  function onRoomCreate(){
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify({
        is_public: isPublic,
        max_players: limit
      }),
    };
    fetch("/api/room-create/", requestOptions)
      .then(response => response.json())
      .then(data => history.push(`/room/${data.code}`, { from: "RoomCreatePage" }));
  }

  return (
    <div class="stworzPokojNapis">
      <Grid container spacing={1}>
        <Grid item xs={12} align="center">
          <Typography component="h4" variant="h4">
            Stwórz pokój gry!
          </Typography>
        </Grid>
        <Grid item xs={12} align="center">
          <FormControl component="fieldset">
            <FormHelperText>
              <div align="center">Prywatność pokoju</div>
            </FormHelperText>
            <RadioGroup
              row
              defaultValue="true"
              onChange={handleRoomPrivacy}
            >
              <FormControlLabel
                value="true"
                control={<Radio color="primary" />}
                label="Publiczny"
                labelPlacement="bottom"
              />
              <FormControlLabel
                value="false"
                control={<Radio color="secondary" />}
                label="Prywatny"
                labelPlacement="bottom"
              />
            </RadioGroup>
          </FormControl>
        </Grid>
        <Grid item xs={12} align="center">
          <FormControl>
            <TextField
              required={true}
              type="number"
              onChange={onPlayersLimitChange}
              defaultValue={4}
              inputProps={{
                min: 2,
                max: 4,
                style: { textAlign: "center" },
              }}
            />
            <FormHelperText>
              <div align="center">Maksymalna liczba graczy</div>
            </FormHelperText>
          </FormControl>
        </Grid>
        <Grid item xs={12} align="center">
          <Button
            color="primary"
            variant="contained"
            onClick={onRoomCreate}
          >
            Stwórz pokój
          </Button>
        </Grid>
      </Grid>
    </div>

  );
}

export default RoomCreatePage;