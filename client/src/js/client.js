import React from "react"
import ReactDOM from "react-dom"
import { Provider } from "react-redux"
import { Route, Switch, HashRouter } from 'react-router-dom';

import Search from "./components/Search"
import store from "./store"
import 'bootstrap/dist/css/bootstrap.min.css'
import './css/style.css'

const app = document.getElementById('app')

ReactDOM.render(
<HashRouter> 
<Provider store={store}>
<Switch>
    <Route exact path="/" component={Search}/>
    {/* <Route path="/movies" component={Profile}/> */}
  </Switch>
</Provider>
</HashRouter>, app);
