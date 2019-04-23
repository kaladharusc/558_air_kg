import React from "react"
import { connect } from "react-redux"

import {searchResearcher} from "../actions/searchAction"

import {Redirect} from "react-router-dom"
@connect((store) => {
    return {
        user_login: store.user_login
    }
})
export default class Search extends React.Component {
    constructor(props) {
        super(props)
    }

    // login() {
    //     console.log(this)
    //     var payload = {
    //         "user" :  {
    //             "email" : this.username,
    //             "password" : this.password
    //         }
    //     }
    //     this.props.dispatch(login(payload))
    // }

    submitRequest() {
        var payload = {
            "researcherName": this.researcherName
        }

        this.props.dispatch(searchResearcher(payload));
    }

    handleChange(event) {
        this[event.target.name] = event.target.value;
    }

    render() {
        return (<div>
            <h1>SEARCH PAGE</h1>
            <input className="input" type="text" name="researcherName" onChange={this.handleChange.bind(this)}></input>
            <button onClick={this.submitRequest.bind(this)}>Search!</button>
        </div>)
    }
}