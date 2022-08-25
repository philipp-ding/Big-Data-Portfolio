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
  <header className='Genres'>
    <div className='TopGenres'>
      <h5> Top 10 Genres according to twitter</h5>
    </div>
    <div className='AllGenres'>
      <h5> All Popular Genres according to twitter</h5>
    </div>
    <div className = "PageInfo">
      <h5 className="ApplicationInfo"> 
      Server: 
      Date:
      Servers Used: 
      Cashed Results:
      </h5>
    </div>
  </header>
  

  <ENTRY_LIST
    messages={messages}
    removeEntry={removeEntryFromState}
  />
  <EntryForm addMessage={addEntryToState} />
</>
);
}; 
 
export default HomePage;