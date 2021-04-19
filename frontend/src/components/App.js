import React from "react";
import { render } from "react-dom";
import StartPage from "./StartPage";
import RoomListPage from "./RoomListPage";

export default function App() {

    return (
        <div className="center">
          <StartPage />
        </div>
      );
  
}

const appDiv = document.getElementById("app");
render(<App />, appDiv);