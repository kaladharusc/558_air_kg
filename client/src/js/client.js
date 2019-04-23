import React from "react"
import ReactDOM from "react-dom"
import { Provider } from "react-redux"
import { Route, Switch, HashRouter } from 'react-router-dom';

import Search from "./components/Search"
import store from "./store"
import 'bootstrap/dist/css/bootstrap.min.css'
import './css/style.css'
import Publications from "./components/Publications";
import Courses from "./components/Courses";

const app = document.getElementById('app')

ReactDOM.render(
<HashRouter> 
<Provider store={store}>
<Switch>
    <Route exact path="/search" component={Search}/>
    <Route exact path="/publications" component={Publications}/>
    <Route exact path="/courses" component={Courses}/>
    {/* <Route path="/movies" component={Profile}/> */}
  </Switch>
</Provider>
</HashRouter>, app);
