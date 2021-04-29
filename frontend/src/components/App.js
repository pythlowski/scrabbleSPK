import React from "react";
import { render } from "react-dom";
import StartPage from "./StartPage";
import RoomListPage from "./roomList/RoomListPage";

export default function App() {

    return (
        <div>
          <StartPage />
        </div>
      );
  
}

const appDiv = document.getElementById("app");
render(<App />, appDiv);