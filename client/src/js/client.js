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
import TreeMap from "./components/TreeMap";

const app = document.getElementById('app')

ReactDOM.render(
<HashRouter>
<Provider store={store}>
<Switch>
    <Route exact path="/search" component={Search}/>
    <Route exact path="/publications" component={Publications}/>
    <Route exact path="/courses" component={Courses}/>
    <Route exact path="/" component={TreeMap}/>
  </Switch>
</Provider>
</HashRouter>, app);
