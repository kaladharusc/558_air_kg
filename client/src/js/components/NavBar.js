import React from "react"
import { connect } from "react-redux"
import {Redirect} from "react-router-dom"

@connect((store) => {
    return {}
})
export default class NavBar extends React.Component {
    render() {
        const {user} = this.props;
        
        return (   
          <nav className="navbar navbar-expand-lg navbar-light">
            <div className="collapse navbar-collapse" id="navbarNavAltMarkup">
              <div className="navbar-nav">
                <a className="nav-item nav-link" href="#/search">Search<span className="sr-only">(current)</span></a>
                <a className="nav-item nav-link" href="#/publications">Publications<span className="sr-only">(current)</span></a>
                <a className="nav-item nav-link" href="#/courses">Courses<span className="sr-only">(current)</span></a>
              </div>
            </div>
          </nav>
            )

    }
}