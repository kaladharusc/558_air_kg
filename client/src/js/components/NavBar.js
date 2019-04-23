import React from "react"
import { connect } from "react-redux"
import {Redirect} from "react-router-dom"

@connect((store) => {
    return {
        user: store.user_login.user,
    }
})
export default class NavBar extends React.Component {
    render() {
        const {user} = this.props;
        
        return (   
            <nav className="navbar navbar-expand-lg navbar-light bg-dark">
            <a className="navbar-brand" href="#">DirectTV NOW</a>
            <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNavAltMarkup">
              <div className="navbar-nav">
                <a className="nav-item nav-link active" href="#/movies">Home <span className="sr-only">(current)</span></a>
                <a className="nav-item nav-link" href="#/friends">Friends <span className="sr-only">(current)</span></a>
                <a className="nav-item nav-link" href="#/explore">Explore <span className="sr-only">(current)</span></a>
              </div>
            </div>
          </nav>
            )

    }
}