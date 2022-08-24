import React from 'react';
import ENTRY_LIST from '../components/Forum/Entry_Details/entry_list';
import EntryForm from '../components/Forum/Entry_Details/entry_form';
import { useContext } from 'react';
import { EntryContext } from '../contexts/Entry_context';



const HomePage = () => {
  const { messages, addEntryToState, removeEntryFromState} = useContext(EntryContext)
 
  console.log(messages);
return (
<>
  
  <ENTRY_LIST
    messages={messages}
    removeEntry={removeEntryFromState}
  />
  <EntryForm addMessage={addEntryToState} />
</>
);
}; 
 
export default HomePage;