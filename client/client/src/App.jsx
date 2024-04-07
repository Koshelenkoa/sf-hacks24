import './App.css';
import Home from './components/Home';
import View from './components/View';
import Layout from './components/Layout';
import AddBlock from './components/AddBlock';
import { Routes, Route} from "react-router-dom";

const App = () => {

  return (
    <div className="App">
        <Routes>
          <Route path="/" element={<Layout/>}>
            <Route index element={<Home/>}/>
            <Route path="/view" element={<View />}/>
            <Route path="/addblock" element={<AddBlock />}/>
          </Route >

        </Routes>
       
      
    </div>
  );
}

export default App;
