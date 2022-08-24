import React, { createContext, useState } from 'react'

export const EntryContext = createContext()

const EntryContextProvider = (props) => {
    
    const [messages, setMessage] = useState([]);

    const addEntryToState = (newEntry) => {
    setMessage([...messages, { ...newEntry, key: messages.length }]);
    };

    const removeEntryFromState = (key) => {
      const newEntries = [...messages];
      newEntries.splice(
        newEntries.findIndex((element) => element.key === key),
        1
      );
    setMessage(newEntries)
    };

    const value = { messages, addEntryToState, removeEntryFromState}
  return (
    <EntryContext.Provider value={value}>
        {props.children}
    </EntryContext.Provider>
    )
}

export default EntryContextProvider