import { Home } from "./Home";
import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";
import { Model } from "./Model";

function App() {

  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path={"/"} element={<Home/>}/> 
          <Route path={"/model/:id"} element={<Model/>}/>
        </Routes>
      </BrowserRouter>
    </div>
  )
}

export default App
