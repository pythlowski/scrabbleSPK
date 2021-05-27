import React from 'react';
import Select from 'react-select'

const options = [
  { value: 'A', label: 'A' },
  { value: 'Ą', label: 'Ą' },
  { value: 'B', label: 'B' },
  { value: 'C', label: 'C' },
  { value: 'Ć', label: 'Ć' },
  { value: 'D', label: 'D' },
  { value: 'E', label: 'E' },
  { value: 'Ę', label: 'Ę' },
  { value: 'F', label: 'F' },
  { value: 'G', label: 'G' },
  { value: 'H', label: 'H' },
  { value: 'I', label: 'I' },
  { value: 'J', label: 'J' },
  { value: 'K', label: 'K' },
  { value: 'L', label: 'L' },
  { value: 'Ł', label: 'Ł' },
  { value: 'M', label: 'M' },
  { value: 'N', label: 'N' },
  { value: 'Ń', label: 'Ń' },
  { value: 'O', label: 'O' },
  { value: 'Ó', label: 'Ó' },
  { value: 'P', label: 'P' },
  { value: 'R', label: 'R' },
  { value: 'S', label: 'S' },
  { value: 'Ś', label: 'Ś' },
  { value: 'T', label: 'T' },
  { value: 'U', label: 'U' },
  { value: 'W', label: 'W' },
  { value: 'Y', label: 'Y' },
  { value: 'Z', label: 'Z' },
  { value: 'Ź', label: 'Ź' },
  { value: 'Ż', label: 'Ż' },
  ]

function BlankSelection({ idx, y, x, dispatch, option }) {
  function onBlankLetterChange(selected) {
    console.log('Zmiana blanka')
    dispatch({type: option, y: y, x: x, letter: selected.value});
  }

  return (
    <div>
      <div>Wybierz literę dla blanka #{idx}</div>
      <Select 
        options={options}
        onChange={onBlankLetterChange}
      />
    </div>
  );
}

export default BlankSelection;