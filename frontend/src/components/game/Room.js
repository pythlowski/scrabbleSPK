import React, { useState, useEffect, useRef, useReducer } from 'react';
import Board from './Board.js';
import MyLetters from './MyLetters.js';
import PlayerElement from './PlayerElement.js';
import BlankSelection from './BlankSelection.js';


const ACTIONS = {
  INIT: 0,
  INIT_ON_CONNECT: 10,
  UPDATE_GRID_FROM_LETTERS: 1,
  UPDATE_HAND: 2,
  SWAP_HAND_HAND: 3,
  SWAP_HAND_BOARD: 4,
  SWAP_BOARD_BOARD: 5,
  FILL_BLANK: 6,
  REVERT_HAND: 8,
  REVERT_BOARD: 9,
  
}

function reducer(lettersData, action){
  switch (action.type) {
    case ACTIONS.INIT:
      return {grid: action.grid, sevenLetters: action.sevenLetters};

    case ACTIONS.SWAP_HAND_HAND:
      var newSevenLetters = lettersData.sevenLetters;
      var letterTmp = newSevenLetters[action.ob1.x].letter;
      newSevenLetters[action.ob1.x].letter = newSevenLetters[action.ob2.x].letter;
      newSevenLetters[action.ob2.x].letter = letterTmp;

      return {grid: lettersData.grid, sevenLetters: newSevenLetters};

    case ACTIONS.SWAP_HAND_BOARD:
      if (action.myTurn){
        var newGrid = lettersData.grid;
        var newSevenLetters = lettersData.sevenLetters;

        var letterTmp = newSevenLetters[action.ob1.x].letter;
        newSevenLetters[action.ob1.x].letter = newGrid[action.ob2.y][action.ob2.x].letter;
        newGrid[action.ob2.y][action.ob2.x].letter = letterTmp;

        return {grid: lettersData.grid, sevenLetters: newSevenLetters};
      }
      return lettersData

    case ACTIONS.SWAP_BOARD_BOARD:
      if (action.myTurn){
        var newGrid = lettersData.grid;

        var letterTmp = newGrid[action.ob1.y][action.ob1.x].letter;
        newGrid[action.ob1.y][action.ob1.x].letter = newGrid[action.ob2.y][action.ob2.x].letter;
        newGrid[action.ob2.y][action.ob2.x].letter = letterTmp;

        return {grid: newGrid, sevenLetters: lettersData.sevenLetters};
      }
      return lettersData

    case ACTIONS.UPDATE_GRID_FROM_LETTERS:
      console.log('Got new letters, updating confirmed on grid!')
      var newGrid = lettersData.grid;
      action.newLetters.forEach(letterObject => {
        newGrid[letterObject.y][letterObject.x].letter = letterObject.letter;
        newGrid[letterObject.y][letterObject.x].confirmed = true;
      })
      return {grid: newGrid, sevenLetters: lettersData.sevenLetters}

    case ACTIONS.UPDATE_HAND:
      var newSevenLetters = lettersData.sevenLetters;
      for (let i = 0; i < 7; i++){
        if (!newSevenLetters[i].letter) {
          newSevenLetters[i] = {
            letter: action.sevenLetters.shift()
          }
        }
      }
      return {grid: lettersData.grid, sevenLetters: newSevenLetters}

    case ACTIONS.FILL_BLANK:
      var newGrid = lettersData.grid;
      newGrid[action.y][action.x].letter = `b${action.letter}`;
      console.log(newGrid[action.y][action.x])
      return {grid: newGrid, sevenLetters: lettersData.sevenLetters}
      
    case ACTIONS.REVERT_HAND:
      console.log('revert hand')
      console.log(action.newSevenLetters)
      console.log(lettersData)
      // return lettersData;

      return {grid: lettersData.grid, sevenLetters: sevenDataFromArray(action.newSevenLetters)}

    case ACTIONS.REVERT_BOARD:
      console.log('revert board')
      var newGrid = lettersData.grid;

      action.lettersToRevert.forEach(letterObject => {
        newGrid[letterObject.y][letterObject.x].letter = '';
        newGrid[letterObject.y][letterObject.x].confirmed = false;
      })
      return {grid: newGrid, sevenLetters: lettersData.sevenLetters}

    case ACTIONS.INIT_ON_CONNECT:
      console.log('init on connect')
      var newGrid = lettersData.grid;

      action.grid.forEach((row, i) => {
        row.forEach((letter, j) =>
        { if (letter) {
          newGrid[i][j].letter = letter;
          newGrid[i][j].confirmed = true;
          }
        })
      })
      return {grid: newGrid, sevenLetters: lettersData.sevenLetters}

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

function sevenDataFromArray(array){
  var sevenLetters = new Array(7);

  for (let i = 0; i < 7; i++){
    sevenLetters[i] = {
      letter: array[i]
    }
  }
  return sevenLetters;
}

function Room(props) {
  const [players, setPlayers] = useState([]);
  const [blanksData, setBlanks] = useState([]);
  const [isHost, setHost] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [myTurn, setMyTurn] = useState(false);
  const [isGameOn, setGameOn] = useState(false);
  const [fillingBlanks, setFillingBlanks] = useState(false);
  const [lettersExchanging, setLettersExchanging] = useState(false);
  const [canQuestion, setCanQuestion] = useState(false);
  const [inBag, setInBag] = useState(0);
  const [toExchange, setToExchange] = useState(new Array(7).fill(false, 0, 7));
  
  const playersCount = useRef(0);
  const myUsername = useRef('');
  const roomCode = useRef(props.match.params.roomCode);
  const socketRef = useRef();
  const selectedField = useRef(null);

  const lettersPoints = useRef({
    ' ': 0, 'A': 1, 'Ą': 5,'B': 3, 'C': 2, 'Ć': 6, 'D': 2, 'E': 1, 'Ę': 5, 'F': 5,'G': 3,'H': 3, 'I': 1, 'J': 3, 'K': 2, 'L': 2, 'Ł': 3, 'M': 2, 'N': 1, 'Ń': 7, 'O': 1, 'Ó': 5,
 'P': 2, 'R': 1, 'S': 1, 'Ś': 5, 'T': 2, 'U': 3, 'W': 1, 'Y': 2, 'Z': 1, 'Ź': 9, 'Ż': 5
  })
  const [lettersData, dispatch] = useReducer(reducer, 
    {
      grid: Array.from(Array(15), _ => Array(15).fill({letter: '', className: 'empty', confirmed: false })), 
      sevenLetters: Array(7).fill({letter: ''})
    }
  )
  
  // console.log(toExchange);
  // console.log(lettersData.grid)
  useEffect(() => {
    // let startGrid = Array.from(Array(15), _ => Array(15).fill({letter: '', wordBonus: 1, letterBonus: 1, confirmed: false }));
    // let startGrid = new Array(15).fill(null).map(()=>new Array(15).fill({letter: '', wordBonus: 1, letterBonus: 1, confirmed: false }));
    
    let gridFromDB = Array.from({ length: 15 }, () => Array.from({ length: 15 }));
    let sevenFromDB = new Array(7);

    var startGrid = gridDataFromArray2D(gridFromDB);
    var startSevenLetters = sevenDataFromArray(sevenFromDB);

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
      const message = data['message'];
      console.log(data)

      if (message == 'init') {
        const data = JSON.parse(e.data);
        console.log('init')
        setPlayers(Array.from(data['players']));
        playersCount.current = data['players'].length;

        setInBag(data['inBag']);
        if (data['isHost']) {
          setHost(true);
          console.log('You are the host');
        }
        console.log('setting username');
        console.log(data['yourUsername']);
        myUsername.current = data['yourUsername'];

        let isPlaying = players.filter(player => player.username == myUsername.current).length;
        setIsPlaying(isPlaying ? true : false);
        setGameOn(data['started']);

        dispatch({type: ACTIONS.INIT_ON_CONNECT, grid: data['grid']});

      }
      else if (message == 'letters') {
        console.log('nowe literki, zara robie dispatch');
        console.log(data['letters'])
        dispatch({type: ACTIONS.UPDATE_GRID_FROM_LETTERS, newLetters: data['letters']});

        setPlayers(players => players.map(player => 
          player.username === data['username'] 
          ? {...player, points : player.points + data['points']} 
          : player ));
        setInBag(inBag => inBag - data['letters'].length > 0 ? inBag - data['letters'].length : 0);
      }
      else if (message == 'new_player') {
        console.log('!!!!!!! dopisuje nowego gracza do listy', data['username']);
        setPlayers(players => [...players, {username: data['username'], points: 0, theirTurn: false, isHost: data['isHost']}])
        playersCount.current += 1;
      }
      else if (message == 'game_start') {
        console.log('game started');
        setGameOn(true);
        setInBag(inBag => inBag - playersCount.current*7);
      }
      else if (message == 'turn_change') {
        console.log('new_turn for player');
        console.log(myTurn)
        if (!myTurn) {
          setCanQuestion(true);
        }

        if (data['username'] == myUsername.current) {
          setMyTurn(true);
          console.log('MY TURN!');
        } else {
          setMyTurn(false);
          console.log("NOT MY TURN :(");
        }
        
        setPlayers(players => players.map(player => 
          player.username === data['username'] 
          ? {...player, theirTurn: true} 
          : {...player, theirTurn: false}));
      }
      else if (message == 'from_bag') {
        console.log('dostałem litery')
        console.log(data['letters']);
        dispatch({type: ACTIONS.UPDATE_HAND, sevenLetters: data['letters']});

      }

      else if (message == 'game_over') {
        console.log("game over")
        alert(`Koniec gry! Wygrywa: ${data['winners']} z ${data['points']} pkt!`)
      }

      else if (message == 'turn_question_response') {
        if (data['incorrect_words'].length > 0) {
          alert(`Wykryto niepoprawne słowa: ${data['incorrect_words']}`);

          dispatch({type: ACTIONS.REVERT_BOARD, lettersToRevert: data['letters_to_revert']});
          setCanQuestion(false);

          setPlayers(players => players.map(player => 
          player.username === data['username'] 
          ? {...player, points : player.points - data['points_to_revert']} 
          : player ));

        } else {
          alert('Poprawny ruch.');
        }
      }

      else if (message == 'revert_details') {
        console.log('Dostaje revert details')
        dispatch({type: ACTIONS.REVERT_HAND, newSevenLetters: data['new_seven_letters']});
        
      }
      
    }

    socketRef.current.onerror = e => {
      console.log('error', e)
    }
  }, []);

  useEffect(() => {
    console.log('nastepuje update listy graczy')
  }, [players]);

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
    if (letters.length >= 1){
      if (!letters.slice(1).every(letter => letter.y == letters[0].y)) return [0,0,0];
      return [letters[0].y, letters[0].x, letters.slice(-1)[0].x];
    }
    return [1,1,1];
  }

  function lettersVertical(letters) {
    if (letters.length >= 1){
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
    if (lettersData.grid.every(row => row.every(field => {if (field.confirmed) return field.letter == ""; return true}))) {
      return letters.length > 1 && letters.some(letter => letter.x == 7 && letter.y == 7)
    } else {
      return letters.some(letter => {
        return [[letter.y, letter.x+1], [letter.y, letter.x-1], [letter.y+1, letter.x], [letter.y-1, letter.x]].some(pair => {
          if (pair[0] >= 0 && pair[0] < 15 && pair[1] >= 0 && pair[1] < 15) return lettersData.grid[pair[0]][pair[1]].confirmed;
          return false;
        });
      });
    }
  }

  function onFieldClick(e) {
    e.preventDefault();
    // var element = e.currentTarget.firstChild
    var element = e.currentTarget;
    var y = element.dataset['y'];
    var x = element.dataset['x'];
    var onBoard = element.dataset['board'] == "true" ? true : false;
    
    if (!lettersExchanging) {
      if (selectedField.current == null) {
        if ((onBoard && !lettersData.grid[y][x].confirmed && lettersData.grid[y][x].letter) || (!onBoard && lettersData.sevenLetters[x].letter)) {
          element.classList.add('selected');
          selectedField.current = {y:y, x:x, onBoard: onBoard, element: element};
        }
      } else if (selectedField.current.x == x && selectedField.current.y == y && selectedField.current.onBoard == onBoard) {
        selectedField.current.element.classList.remove('selected')
        selectedField.current = null;
        console.log('klikam to samo drugi raz')
      } else {
        if (selectedField.current.onBoard && onBoard && !lettersData.grid[y][x].confirmed) {
          dispatch({type: ACTIONS.SWAP_BOARD_BOARD, ob1: selectedField.current, ob2: {y:y, x:x}, myTurn: myTurn});
          selectedField.current.element.classList.remove('selected');
          selectedField.current = null;
          console.log('zamieniam na boardzie i na boardzie')
        } else if (!selectedField.current.onBoard && !onBoard) {
          dispatch({type: ACTIONS.SWAP_HAND_HAND, ob1: selectedField.current, ob2: {y:y, x:x}});
          selectedField.current.element.classList.remove('selected');
          selectedField.current = null;
        } else if (selectedField.current.onBoard && !onBoard) {
          dispatch({type: ACTIONS.SWAP_HAND_BOARD, ob1: {y:y, x:x}, ob2: selectedField.current, myTurn: myTurn});
          selectedField.current.element.classList.remove('selected');
          selectedField.current = null;
        } else if (!selectedField.current.onBoard && onBoard && !lettersData.grid[y][x].confirmed) {
          dispatch({type: ACTIONS.SWAP_HAND_BOARD, ob1: selectedField.current, ob2: {y:y, x:x}, myTurn: myTurn});
          selectedField.current.element.classList.remove('selected');
          selectedField.current = null;
        }
      }
    } else if (!onBoard) {
      // if (!toExchange[x]) {
      //   element.classList.add('selected-to-exchange');
      // } else {
      //   element.classList.remove('selected-to-exchange');
      // }
      setToExchange(data => data.map((element, index) => 
        index == x 
        ? !element 
        : element ));
      // zaznaczanie liter do wymiany
    }
  }

  function onGameStart(){
    console.log('przyciskam start');
    socketRef.current.send(JSON.stringify({
      'message': 'game_start'
    }));
  }

  function sendLetters(){
    console.log('chcę wysłać litery!!')
    const letters = getAddedLetters();
    if (legalLetters(letters)) {
      console.log('correct letters setup!');

      var blanks = letters.filter(letter => letter.letter == ' ');
        if (blanks.length) {
          console.log('Są jakieś niewypełnione blanki!')
          if (!fillingBlanks){
            console.log('Pierwsza próba wysłania, teraz pojawią się pola do wybrania liter')
            setFillingBlanks(true);
            setBlanks(blanks);
          }
        }
        else {
          console.log('All OK, sending letters to the server!');
          socketRef.current.send(JSON.stringify({
            'message': 'letters',
            'letters': letters
          }));
          setFillingBlanks(false);
          setBlanks([]);
          // setMyTurn(false);
        }
    } else {
      alert('Nielegalne ustawienie liter!');
    }
  }

  function onTurnSkip(){
    socketRef.current.send(JSON.stringify({
      'message': 'turn_skip'
    }));
  }

  function onLettersExchange(){
    setLettersExchanging(true);
    console.log('wymieniam litery')
    // wszystkie litery nie confirmed z boarda wrzuć na rękę
  }

  function sendLettersToExchange() {
    var lettersToExchange = [];
    
    for (let i = 0; i < 7; i++) {
      if(toExchange[i]) {
        lettersToExchange.push(lettersData.sevenLetters[i].letter);
      }
    }
    
    if (lettersToExchange.length == 0) {
      alert('Nie wybrano liter.');
    }
    else if (lettersToExchange.length <= inBag) {
      
      socketRef.current.send(JSON.stringify({
        'message': 'letters_exchange',
        'letters': lettersToExchange
      }));
      
      for (let i = 0; i < 7; i++) {
        if(toExchange[i]) {
          lettersData.sevenLetters[i] = {letter: ''};
        }
      }

      setToExchange(new Array(7).fill(false, 0, 7));
      setLettersExchanging(false);

    } else {
      alert('Nie ma tylu liter w worku!');
    }
  }

  function onExchangeCancel() {
    setLettersExchanging(false);
    setToExchange(new Array(7).fill(false, 0, 7));
  }

  function questionPreviousLetters() {
    socketRef.current.send(JSON.stringify({
        'message': 'question_turn'
      }));
  }

  return (
    <div id='room'>
      <div className='a1'>
        
        <h4>{roomCode.current}</h4>

        <Board grid={lettersData.grid} lettersPoints={lettersPoints.current} onFieldClick={onFieldClick} />
        <MyLetters letters={lettersData.sevenLetters} lettersPoints={lettersPoints.current} toExchange={toExchange} onFieldClick={onFieldClick} />
        
      </div>
      

      
      <div className='a2'>
        {players.map((player, index) => <PlayerElement key={index} playerName={player.username} points={player.points} theirTurn={player.theirTurn} isHost={player.isHost}/> )}
        
        {isHost && !isGameOn && 
          <React.Fragment>
            <button onClick={onGameStart}>ROZPOCZNIJ GRĘ</button>
          </React.Fragment>
        }
        
        {!isHost && !isGameOn && 
          <React.Fragment>
            <div>Oczekiwanie. Host musi rozpocząć grę.</div>
          </React.Fragment>
        }

        {isGameOn && myTurn && !lettersExchanging &&
          <React.Fragment>
            <button onClick={sendLetters}>POTWIERDŹ</button>
            <button onClick={onTurnSkip}>OPUŚĆ KOLEJKĘ</button>
            <button onClick={onLettersExchange}>WYMIEŃ LITERY</button>            
          </React.Fragment>
        } 

        {isGameOn && myTurn && lettersExchanging && 
          <React.Fragment>
            <button onClick={sendLettersToExchange}>WYMIEŃ LITERY</button>
            <button onClick={onExchangeCancel}>ANULUJ</button>          
          </React.Fragment>
        }
        <div>Pozostało liter w worku: {inBag}</div>

        {isGameOn && isPlaying &&
          <button onClick={questionPreviousLetters} disabled={!canQuestion}>ZAKWESTIONUJ UŁOŻONE SŁOWA</button>
        }

        {!isPlaying &&
          <div>Jesteś obserwatorem gry.</div>
        }
        
        {blanksData.map((letter, index) => 
          <BlankSelection key={index+1} idx={index+1} y={letter.y} x={letter.x} dispatch={dispatch} option={ACTIONS.FILL_BLANK}/>
        )}

      </div>

    </div>
  );
}

export default Room;