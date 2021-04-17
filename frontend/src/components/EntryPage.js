import React, { Component, useEffect, useState } from "react";
import { render } from "react-dom";

function EntryPage(props) {

    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        setLoading(true);
        fetch("api/room-list")
        .then(response => response.json())
        .then(data => {
            setData(data);
            setLoading(false);
        });
    }, []);

    return ( 
    <div>
        <p>HELLO3!</p>
        {loading && <p>Loading data...</p>}
        <ul>
        {data.map(room => <li key={room.id}>{room.code} - {room.host}</li>)}
        </ul>
    </div>
    );
  
}

export default EntryPage;

const container = document.getElementById("app");
render(<EntryPage />, container);