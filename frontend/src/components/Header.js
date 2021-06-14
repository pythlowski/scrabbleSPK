import React from 'react';
import { Grid, Button, Typography } from "@material-ui/core";
import { useHistory } from "react-router-dom";

function Header(props) {
  const history = useHistory();

  return (
    <div class="menuglowne"> 
      <Grid container spacing={3}>

        <Grid item xs={3}>
          <Typography component="h4" variant="h4">
            Scrabble ONLINE        
          </Typography>
        </Grid>

        <Grid item xs={3}>
          <Button 
            color="primary"
            onClick={() => history.push("/create")}
          >
            Stwórz pokój
          </Button> 
        </Grid>

        <Grid item xs={3}>
          <Button 
            color="primary"
            onClick={() => history.push("/list")}
          >
            Lista pokoi
          </Button>
        </Grid>
        
        <Grid item xs={3}>
          <Button 
            color="primary"
            onClick={() => history.push("/")}
          >
            Zmień nick
          </Button>
        </Grid>
    
      </Grid>
    </div>

  );
}

export default Header;