import React from 'react';
import Square from './Square.js';
import MyLetters from './MyLetters.js';



function Board(props) {

    var tmp_coords = []

    function passTheCoords (x, y) {
        tmp_coords.push([x, y])
        console.log(tmp_coords.toString());


      }

      //grid[row].push(<Square  type="start" letter="Null" />) --na pamiątkę

    function createGrid() {
        const grid = []
        for (let row = 0; row < 15; row ++) {
            grid.push([])
            for (let col = 0; col < 15; col ++) {
                if (row ==7 && col == 7){
                    grid[row].push(<Square x={row} y={col} key={`${col}${row}`} type="start" letter="Null" passTheCoords = {passTheCoords} />)
                }
                else if (row ==1 && col == 7 ){
                    grid[row].push(<Square  x={row} y={col} key={`${col}${row}`} type="bonus" letter="Null" passTheCoords = {passTheCoords}/>)

                }
                else
                    grid[row].push(<Square  x={row} y={col} key={`${col}${row}`} type="normal" letter="Null" passTheCoords = {passTheCoords}/>)
            }
        }
        return grid;
      }
    
      const grid = createGrid()

    return (
        <div>
            <div className='grid-board'>
                {grid}
            </div>

            {/*<div>
                <p align='right'>{grid[1][1]}</p>
            </div>
            */}
            <div className='letters-board' align='right'>
                <MyLetters />  
            </div>
        </div>
      );
}

export default Board;