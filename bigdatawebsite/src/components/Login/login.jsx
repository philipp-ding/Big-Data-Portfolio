import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import "../Login/login.css"

const LoginForm = ({ addUser }) => {
  const [name, setName] = useState('');
  const [lastname, setLastName] = useState('');
  const [email, setEmail] = useState('');
  let navigate = useNavigate();

  return (
    <>
    <div className="LoginBox">
      
        <label className ="Login-Text">Name: </label>
        <input
          type='text'
          name='name'
          className='name'
          value={name}
          onChange={(e) => setName(e.target.value)}></input>
      
      
        <label className ="Login-Text">Lastname: </label>
        <input
          type='text'
          name='lastname'
          className='lastname'
          value={lastname}
          onChange={(e) => setLastName(e.target.value)}></input>
     
        <label className ="Login-Text" >E-Mail: </label>
        <input
          type='text'
          name='email'
          className='email'
          value={email}
          onChange={(e) => setEmail(e.target.value)}></input>
      
      {name !== '' ? (
        <button 
          type= "button"
          className="button"
          onClick={() => navigate(`/home/${name}${lastname}`, {state:{name: name, lastname: lastname, email:email}})}>
          Log in
        </button>
      ) : null}
      {name === '' ? (
        <button 
          type= "button"
          className="button"
          onClick={() => navigate(`*${name}${lastname}`, {state:{name: name, lastname: lastname, email:email}})}>
          Log in
        </button>
      ) : null}
    </div></>
  );
};

export default LoginForm;
