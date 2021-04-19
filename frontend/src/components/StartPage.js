import React from "react";
import NicknamePage from "./NicknamePage";
import RoomListPage from "./RoomListPage";
import RoomCreatePage from "./RoomCreatePage";
import Room from "./Room";

import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link,
    Redirect,
  } from "react-router-dom";

function StartPage(props) {
    return (
        <Router>
        <Switch>
          <Route exact path="/" component={NicknamePage} />
          <Route path="/list" component={RoomListPage} />
          <Route path="/create" component={RoomCreatePage} />
          <Route path="/room/:roomCode" component={Room} />
        </Switch>
      </Router>
      );
}

export default StartPage;