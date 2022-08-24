import React from "react";
import './entry_list.css';
import { useLocation } from "react-router-dom";

import TextEntry from './Entry/text_entry';
const ENTRY_LIST = ({ messages, removeEntry }) => {
 
  const location = useLocation();
  const state = (location.state?location.state:{name:"", lastname: "", email:""})
  const {name, lastname, email} = state;
  return (
    
      <>{messages.map((value) => {
        return (
          <div className='grid-cols-3'>
            <React.Fragment key={value.key}>
              <TextEntry name={value.name} lastname={value.lastname} email={value.email} body={value.Message}/>
              {value.name ===name && value.lastname===lastname && value.email===email ?(
                <button 
                  type="button"
                  className="button"
                  onClick={() => removeEntry(value.key)}>
                  Remove Entry
                </button>
              ):null}
            </React.Fragment>
          </div>);
      })}
    </>
  );
};

export default ENTRY_LIST;
