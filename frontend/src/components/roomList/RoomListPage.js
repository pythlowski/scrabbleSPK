import React, { useEffect, useState } from "react";
import RoomElement from "./RoomElement";
import { Grid, Button, TextField, Typography, Paper, Table, TableContainer, TableHead, TableRow, TableCell, TableBody } from "@material-ui/core";
import { useHistory } from "react-router-dom";
function RoomListPage() {

  const [rooms, setRooms] = useState([]);
  const [roomCode, setRoomCode] = useState('');
  const [loading, setLoading] = useState(false);

  const history = useHistory();

  useEffect(() => {
    setLoading(true);
    fetch("api/room-list/")
    .then(response => response.json())
    .then(data => {
      setRooms(data);
      setLoading(false);
    });
  }, []);

  function onRoomCodeChange(e) {
    setRoomCode(e.target.value);
  }

  function onCustomRoomCodeJoin(e) {
    history.push(`/room/${roomCode.trim()}`, { from: "RoomListPage" })
  }

  return ( 
    <div class="stworzPokojNapis">
      <Grid container spacing={1}>
        <Grid item xs={12} align="center">
          <Typography component="h3" variant="h3">
            Wszystkie aktywne pokoje gier!
          </Typography>
        </Grid>

        <Grid item xs={12} align="center">
          <Grid container spacing={2}>
            <TextField
              value={roomCode}
              onChange={onRoomCodeChange}
            />

            <Button 
              color="primary" 
              variant="contained"
              onClick={onCustomRoomCodeJoin}>
                DOŁĄCZ
            </Button>
          </Grid>
        </Grid>

        {loading &&
          <Grid item xs={12} align="center">
            <Typography component="h4" variant="h4">
              Ładowanie danych...
            </Typography>
          </Grid>
        }
        {!loading &&
            <Grid item xs={12} align="center">
              <TableContainer component={Paper}>
                <Table className="rooms-table" aria-label="simple table">
                  <TableHead>
                    <TableRow>
                      <TableCell></TableCell>
                      <TableCell align="right">Kod pokoju</TableCell>
                      <TableCell align="right">Nazwa pokoju</TableCell>
                      <TableCell align="right">Limit graczy</TableCell>
                    </TableRow>
                  </TableHead>

                  <TableBody>
                    {rooms.map(room => RoomElement(room))}
                  </TableBody>
                </Table>
              </TableContainer>
            </Grid>
        }
      </Grid>
    </div>
  );

}

export default RoomListPage;