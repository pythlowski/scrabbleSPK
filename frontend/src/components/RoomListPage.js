import React, { useEffect, useState } from "react";

function RoomListPage() {

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
        {data.map(room => <li key={room.id}>{room.code} - {room.host} XD</li>)}
        </ul>
    </div>
    );
  
}

export default RoomListPage;