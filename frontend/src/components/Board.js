import React from 'react';
import Square from './Square.js';


function Board(props) {


    function createGrid() {
        const grid = []
        for (let row = 0; row < 15; row ++) {
            grid.push([])
            for (let col = 0; col < 15; col ++) {
                if (row ==7 && col == 7){
                    grid[row].push(<Square key={`${col}${row}`} type="start" letter="Null" />)
                }
                else if (row ==1 && col == 7 ){
                    grid[row].push(<Square key={`${col}${row}`} type="bonus" letter="Null"/>)

                }
                else
                    grid[row].push(<Square key={`${col}${row}`} type="normal" letter="Null"/>)
            }
        }
        return grid;
      }
    
      const grid = createGrid()

    return (
        <div><div className='grid-board'>
            {grid}
            
        </div>
        <div><p align='right'>{grid[1][1]}</p>
            </div>
            </div>
      );
}

export default Board;