import './App.css';
import HomePage from './pages/HomePage'
import StartingPage from './pages/StartingPage'

import Outlet from './components/Outlet';
import { Routes, Route, Link } from 'react-router-dom';
import EntryContextProvider from './contexts/Entry_context';



function App() {
  return (
    <div className="App">
      <EntryContextProvider>
        <header className='App-header'>
          <div className="Header_Box">
            
            <div className="Inner_Box">
              <nav>
                <Link to=''className="StartingPage">Login</Link>
                <Link to='home' className="HomePage">Home</Link>
              </nav>
            </div>
            <div className="Inner_Box">
              <h3 className="Headline">Genre's Popularity based on Tweets</h3>
            </div>
            <div className='Inner_Box'>
            
            </div>
          </div>
        </header>
        <Routes>
          <Route path='/' element={<StartingPage />} />
          <Route path='/home' element={<HomePage />}>
            <Route path=':id' element={<Outlet />} />
          </Route>
          
        </Routes>
      </EntryContextProvider>

    </div>
      );
}

export default App;

