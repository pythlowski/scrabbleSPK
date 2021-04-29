import React, { useEffect, useState } from "react";
import RoomElement from "./RoomElement";
import { Grid, Button, Typography, Paper, Table, TableContainer, TableHead, TableRow, TableCell, TableBody } from "@material-ui/core";
import { useHistory } from "react-router-dom";

function RoomListPage() {

  const [rooms, setRooms] = useState([]);
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

  return ( 
    <Grid container spacing={1}>
      <Grid item xs={12} align="center">
        <Typography component="h3" variant="h3">
          Wszystkie aktywne pokoje gier!
        </Typography>
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
                  <TableCell align="right">Gracze</TableCell>
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
  );

}

export default RoomListPage;