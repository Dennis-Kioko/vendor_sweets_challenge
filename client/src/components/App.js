import { Switch, Route } from "react-router-dom";
import Header from "./Header";
import Vendor from "./Vendor";
import Home from "./Home";

function App() {
  return (
    <div>
      <Header />
      <main>
        <Switch>
          <Route exact path="/vendors/:id">
            <Vendor />
          </Route>
          <Route exact path="/">
            <Home />
          </Route>
        </Switch>
      </main>
    </div>
  );
}

export default App;