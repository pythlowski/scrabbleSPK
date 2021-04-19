import React from 'react';
import { Button, TableRow, TableCell } from "@material-ui/core";
import { useHistory } from "react-router-dom";

function RoomElement(props) {
  const { code, host_name, current_players, max_players } = props;
  
  const history = useHistory();

  function onRoomSelection(e) {
    history.push(`/room/${code}`, { from: "RoomListPage" })
  }

  return (
    <TableRow key={code}>
        <TableCell component="th" scope="row">
          <Button color="primary" onClick={onRoomSelection}>DOŁĄCZ</Button>
        </TableCell>
        <TableCell align="right">{code}</TableCell>
        <TableCell align="right">Pokój użytkownika {host_name}</TableCell>
        <TableCell align="right">{current_players}/{max_players}</TableCell>
      </TableRow>
  );
}

export default RoomElement;