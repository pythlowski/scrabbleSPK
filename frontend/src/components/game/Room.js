import React, { useState, useEffect, useRef, useReducer } from 'react';
import Board from './Board.js';
import MyLetters from './MyLetters.js';
import PlayerElement from './PlayerElement.js';
import { TextField, Button, Grid } from "@material-ui/core";

const ACTIONS = {
  INIT: 0,
  SWAP: 1,
  UPDATE_GRID: 2,
  UPDATE_HAND: 3,
}

function reducer(lettersData, action){
  switch (action.type) {
    case ACTIONS.INIT:
      return {grid: action.grid, sevenLetters: action.sevenLetters};
    case ACTIONS.SWAP:
      var newGrid = lettersData.grid;
      var newSevenLetters = lettersData.sevenLetters;
      var letterTmp;

      var x1 = action.ob1.x;
      var x2 = action.ob2.x;
      var y1 = action.ob1.y;
      var y2 = action.ob2.y;
      
      if (action.ob1.onBoard && action.ob2.onBoard) {
        console.log('swapping on board and on board')
        letterTmp = newGrid[y1][x1].letter;
        newGrid[y1][x1].letter = newGrid[y2][x2].letter;
        newGrid[y2][x2].letter = letterTmp;

      } else if (action.ob1.onBoard && !action.ob2.onBoard) {
        console.log('swapping on board and on 7')
        letterTmp = newGrid[y1][x1].letter;
        newGrid[y1][x1].letter = newSevenLetters[x2].letter;
        newSevenLetters[x2].letter = letterTmp;

      } else if (!action.ob1.onBoard && action.ob2.onBoard) {
        console.log('swapping on 7 and on board')
        letterTmp = newSevenLetters[x1].letter;
        newSevenLetters[x1].letter = newGrid[y2][x2].letter;
        newGrid[y2][x2].letter = letterTmp;
      }
      return {grid: newGrid, sevenLetters: newSevenLetters};
    case ACTIONS.UPDATE_GRID:
      return {grid: gridDataFromArray2D(action.grid), sevenLetters: sevenLetters}
    case ACTIONS.UPDATE_HAND:
      return {grid: grid, sevenLetters: action.sevenLetters}
    default:
      return lettersData;
  }
}

function gridDataFromArray2D(array2D){
  
  var Grid = Array.from({ length: 15 }, () => Array.from({ length: 15 }));
  for (let i = 0; i < 15; i++) {
    for (let j = 0; j < 15; j++) {
      Grid[i][j] = {
        letter: array2D[i][j] ? array2D[i][j] : '',
        className: array2D[i][j] ? 'filled' : 'empty',
        confirmed: array2D[i][j] ? true : false
      }
    }
  }
  return Grid;

}

function sevenDataFromArray2D(array){
  var sevenLetters = new Array(7);

  for (let i = 0; i < 7; i++){
    sevenLetters[i] = {
      letter: array[i]
    }
  }
  return sevenLetters;
}

function Room(props) {
  console.log('render :)')
  const [players, setPlayers] = useState([]);
  const roomCode = useRef(props.match.params.roomCode);
  const socketRef = useRef();
  const selectedField = useRef(null);
  const lettersPoints = useRef({
    'A': 1, 'Ą': 5,'B': 3, 'C': 2, 'Ć': 6, 'D': 2, 'E': 1, 'Ę': 5, 'F': 5,'G': 3,'H': 3, 'I': 1, 'J': 3, 'K': 2, 'L': 2, 'Ł': 3, 'M': 2, 'N': 1, 'Ń': 7, 'O': 1, 'Ó': 5,
 'P': 2, 'R': 1, 'S': 1, 'Ś': 5, 'T': 2, 'U': 3, 'W': 1, 'Y': 2, 'Z': 1, 'Ź': 9, 'Ż': 5, ' ': 0
  })
  const [lettersData, dispatch] = useReducer(reducer, 
    {
      grid: Array.from(Array(15), _ => Array(15).fill({letter: '', className: 'empty', confirmed: false })), 
      sevenLetters: Array(7).fill({letter: ''})
    }
  )
  
  useEffect(() => {
    // let startGrid = Array.from(Array(15), _ => Array(15).fill({letter: '', wordBonus: 1, letterBonus: 1, confirmed: false }));
    // let startGrid = new Array(15).fill(null).map(()=>new Array(15).fill({letter: '', wordBonus: 1, letterBonus: 1, confirmed: false }));
    
    setPlayers([{nickname: 'zbycholud', points: 210}, {nickname: 'zbycholud2', points: 2102}]);
    let gridFromDB = Array.from({ length: 15 }, () => Array.from({ length: 15 }));
    let sevenFromDB = new Array(7);

    gridFromDB[10][5] = 'A';
    gridFromDB[10][6] = 'B';
    gridFromDB[10][7] = 'C';
    gridFromDB[10][8] = 'D';
    gridFromDB[10][9] = 'Ę';
    gridFromDB[11][9] = 'Ó';
    gridFromDB[3][3] = 'O';

    sevenFromDB[0] = 'A';
    sevenFromDB[1] = 'I';
    sevenFromDB[2] = 'D';
    sevenFromDB[3] = 'S';

    var startGrid = gridDataFromArray2D(gridFromDB);
    var startSevenLetters = sevenDataFromArray2D(sevenFromDB);

    var tripleWords = [[0,0], [0,7], [0,14], [7,0], [7,14], [14,0], [14,7], [14,14]];
    var doubleWords = [[7,7], [1,1], [2,2], [3,3], [4,4], [10,10], [11,11], [12,12], [13,13], [1,13], [2,12], [3,11], [4,10], [13,1], [12,2], [11,3], [10,4]];
    var tripleLetters = [[1,5], [1,9], [5,1], [5, 5], [5, 9], [5, 13], [9, 1], [9, 5], [9, 9], [9, 13], [13, 5], [13, 9]];
    var doubleLetters = [[0,3], [0,11], [2,6], [2,8], [3,0], [3,7], [3,14], [6,2], [6,6], [6,8], [6,12], [7,3], [7,11], [8,2], [8,6], [8,8], [8, 12], [11, 0], [11, 7], [11, 14], [12, 6], [12, 8], [14, 3], [14, 11]];

    tripleWords.forEach(pair => { if(!startGrid[pair[0]][[pair[1]]].letter) startGrid[pair[0]][[pair[1]]].className = 'triple-word'; });
    doubleWords.forEach(pair => { if(!startGrid[pair[0]][[pair[1]]].letter)  startGrid[pair[0]][[pair[1]]].className = 'double-word'; });
    tripleLetters.forEach(pair => { if(!startGrid[pair[0]][[pair[1]]].letter) startGrid[pair[0]][[pair[1]]].className = 'triple-letter'; });
    doubleLetters.forEach(pair => { if(!startGrid[pair[0]][[pair[1]]].letter) startGrid[pair[0]][[pair[1]]].className = 'double-letter'; });

    dispatch({type: ACTIONS.INIT, grid: startGrid, sevenLetters: startSevenLetters});

    socketRef.current = new WebSocket(
      'ws://' +
      window.location.host +
      '/ws/game/' +
      roomCode.current +
      '/'
    )
    socketRef.current.onopen = e => {
      console.log('open', e)
    }

    socketRef.current.onmessage = e => {
      const data = JSON.parse(e.data);
      console.log(data)
    }

    socketRef.current.onerror = e => {
      console.log('error', e)
    }
  }, []);

  useEffect(() => {
    console.log('lettersData sie zmienilo')
  }, [lettersData])

  function getAddedLetters() {
    var letters = [];
    
    for (let i = 0; i < 15; i++) {
      for (let j = 0; j < 15; j++) {
        if (lettersData.grid[i][j].letter && !lettersData.grid[i][j].confirmed) {
          letters.push({letter: lettersData.grid[i][j].letter, y: i, x: j});
        }
      }
    }
    return letters;
  }

  function legalLetters(letters){
    if(legalLettersHorizontal(letters)) return true;
    else return legalLettersVertical(letters);
  }

  function legalLettersHorizontal(letters){
    var [y, startX, endX] = lettersHorizontal(letters);

    if (y === startX && y === endX && y == 1){
      return false;
    } else if (y === startX && y === endX && y == 0) {
      return false;
    } else {
      if (noSpaceBetweenLettersHorizontal(y, startX, endX)) return lettersTouchConfirmedOnes(letters);
      return false;
    }
  }

  function legalLettersVertical(letters){
    var [x, startY, endY] = lettersVertical(letters);
    // console.log(x, startY, endY);
    if (x === startY && x === endY && x == 1){
      console.log('1 lub 0 liter');
      return false;
    } else if (x === startY && x === endY && x == 0) {
      console.log('litery nie w linii');
      return false;
    } else {
      if (noSpaceBetweenLettersVertical(x, startY, endY)) return lettersTouchConfirmedOnes(letters);
      return false;
    }
  }
  
  function lettersHorizontal(letters) {
    if (letters.length > 1){
      if (!letters.slice(1).every(letter => letter.y == letters[0].y)) return [0,0,0];
      return [letters[0].y, letters[0].x, letters.slice(-1)[0].x];
    }
    return [1,1,1];
  }

  function lettersVertical(letters) {
    if (letters.length > 1){
      if (!letters.slice(1).every(letter => letter.x == letters[0].x)) return [0,0,0];
      return [letters[0].x, letters[0].y, letters.slice(-1)[0].y];
    }
    return [1,1,1];
  }

  function noSpaceBetweenLettersHorizontal(y, startX, endX) {
    for(let j=startX; j < endX; j++){
      if (!lettersData.grid[y][j].letter) return false;
    }
    return true;
  }

  function noSpaceBetweenLettersVertical(x, startY, endY) {
    for(let i=startY; i < endY; i++){
      if (!lettersData.grid[i][x].letter) return false;
    }
    return true;
  }

  function lettersTouchConfirmedOnes(letters){
    return letters.some(letter => {
      return [[letter.y, letter.x+1], [letter.y, letter.x-1], [letter.y+1, letter.x], [letter.y-1, letter.x]].some(pair => {
        if (pair[0] >= 0 && pair[0] < 15 && pair[1] >= 0 && pair[1] < 15) return lettersData.grid[pair[0]][pair[1]].confirmed;
        return false;
      });
    });
  }

  function onFieldClick(e) {
    e.preventDefault();
    // var element = e.currentTarget.firstChild
    var element = e.currentTarget;
    // const letter = element.innerText;
    var y = element.dataset['y'];
    var x = element.dataset['x'];
    var onBoard = element.dataset['board'] == "true" ? true : false;

    if (selectedField.current == null) {
      if ((onBoard && !lettersData.grid[y][x].confirmed && lettersData.grid[y][x].letter) || (!onBoard && lettersData.sevenLetters[x].letter)) {
        element.className += 'selected';
        selectedField.current = {y:y, x:x, onBoard: onBoard, element: element};
      }
    } else if (!(selectedField.current.x == x && selectedField.current.y == y && selectedField.current.onBoard == onBoard)) {
      if (
        (selectedField.current.onBoard && onBoard && !lettersData.grid[y][x].confirmed) ||
        (!selectedField.current.onBoard && !onBoard) ||
        (selectedField.current.onBoard && !onBoard) ||
        (!selectedField.current.onBoard && onBoard && !lettersData.grid[y][x].confirmed)
      ) {
        dispatch({type: ACTIONS.SWAP, ob1: selectedField.current, ob2: {y:y, x:x, onBoard: onBoard}});
        selectedField.current.element.classList.remove('selected');
        selectedField.current = null;
      }
    }
  }

  function sendLetters(){
    const letters = getAddedLetters();
    if (legalLetters(letters)) {
      console.log('correct letters setup!');
      socketRef.current.send(JSON.stringify({
        'message': 'letters',
        'letters': 'xd'
      }));
    }
  }

  function onTurnSkip(){
    // send to ws skip
  }

  function onLettersExchange(){
    // send to ws and get new letters 
  }

  return (
    <div id='room'>
      <div className='inline'>
        <h4>{roomCode.current}</h4>

        <Board grid={lettersData.grid} lettersPoints={lettersPoints.current} onFieldClick={onFieldClick} />
        <MyLetters letters={lettersData.sevenLetters} lettersPoints={lettersPoints.current} onFieldClick={onFieldClick} />
      </div>

      <div className='inline'>
        <div>
          {players.map(player => <PlayerElement key={player.nickname} playerName={player.nickname} points={player.points}/> )}
          <button onClick={sendLetters}>POTWIERDŹ</button>
          <button onClick={onTurnSkip}>OPUŚĆ KOLEJKĘ</button>
          <button onClick={onLettersExchange}>WYMIEŃ LITERY</button>

        </div>
      </div>

    </div>
  );
}

export default Room;