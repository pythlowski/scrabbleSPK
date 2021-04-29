import React from "react";
import NicknamePage from "./NicknamePage";
import RoomListPage from "./roomList/RoomListPage";
import RoomCreatePage from "./RoomCreatePage";
import Room from "./game/Room";
import Header from "./Header";

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
          <Header />
          <div className="center">
            <Switch>
              <Route exact path="/" component={NicknamePage} />
              <Route path="/list" component={RoomListPage} />
              <Route path="/create" component={RoomCreatePage} />
              <Route path="/room/:roomCode" component={Room} />
            </Switch>
          </div>
      </Router>
      );
}

export default StartPage;