import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import "../Entry_Details/entry_form.css"

const EntryForm = ({ addMessage }) => {
  const [Message, setMessage] = useState('');

 
  const location = useLocation();
  const state = (location.state?location.state:{name:"", lastname: "", email:""})
  const {name, lastname, email} =state;
  return (
    <><div className="MessageBox"> 
      <div>
        <label className="Message-Text">Message: </label>
        <input
          type='text'
          name='message'
          className="message"
          value={Message}
          onChange={(e) => setMessage(e.target.value)}></input>
      </div>
      {Message !== '' ? (
        <button 
          type="button"
          className="button"
          onClick={() => addMessage(({ name:name, lastname:lastname, email:email, Message: Message }))}>
          Add Message
        </button>
      ) : null}
    </div></>
  );
};

export default EntryForm;
