import React from "react"
import { connect } from "react-redux"

import {searchPublications} from "../actions/publicationSearchAction"
import {fuzzySearchResearcher} from "../actions/fuzzySearchAction";
import NavBar from "./NavBar";

import {Redirect} from "react-router-dom"
@connect((store) => {
    return {
        publicationDetails: store["publicationReducer"].publicationDetails
    }
})

export default class Publications extends React.Component {
    constructor(props) {
        super(props);
        this.buttons = {
            'ai': 0,
            'vision': 0,
            'ml': 0,
            'nlp': 0,
            'ir': 0
        }
    }

    handleChange(event) {
        this.buttons[event.target.value] = this.buttons[event.target.value] ^ 1;
        console.log(this.buttons);
    }

    submitRequest() {

        var searchQueryParams = "";

        Object.keys(this.buttons).forEach((key) => {
            if (this.buttons[key] == 1) {
                searchQueryParams += `(${key})*`;
            }
        })
        if (searchQueryParams != "") {
            console.log(searchQueryParams);
            var payload = {
                "searchQueryParams": searchQueryParams
            }
            this.props.dispatch(searchPublications(payload));
        } else {
            console.log("No radio button selected");
        }
    }

    render() {
        var {publicationDetails} = this.props;
        return (
            <div>
                <NavBar/>
                <h1>Publications List page</h1>
                <input type="checkbox" onChange={this.handleChange.bind(this)} value="ai"/> AI<br/>
                <input type="checkbox" onChange={this.handleChange.bind(this)} value="vision"/> VISION<br/>
                <input type="checkbox" onChange={this.handleChange.bind(this)} value="mlmining"/> ML AND DATA Mining<br/>
                <input type="checkbox" onChange={this.handleChange.bind(this)} value="nlp"/> NLP<br/>
                <input type="checkbox" onChange={this.handleChange.bind(this)} value="ir"/> IR<br/>
                <button onClick={this.submitRequest.bind(this)}>Search!</button>

                {
                    Object.keys(publicationDetails).length === 0 && publicationDetails.constructor === Object ?
                    (<div id="publicationDetails">Empty Publications</div>)
                    :(<PublicationDetailsComponent publicationDetails={publicationDetails.slice(0, 50)}/>)
                }

            </div>

        )
    }
}

function PublicationDetailsComponent(props) {

    return (
      <div id="courseDetails">
        <br/>
        <br/>
        {/* <BootstrapTable keyField='id' data={ props.courseDetails } columns={ columns } striped hover condensed/> */}
        <table className="table table-bordered table-hover" width="100%">
            <tbody>
            {props.publicationDetails.map((row, key) => {
                return <TableRow row={row} key={key}/>
            })}
            </tbody>
        </table>
      </div>
    )
}

const TableRow = ({row, key}) => {
    console.log(row);
    return (
    <tr key={key}>
        {Object.values(row).map((cell, key) => {
           return <TableCell cell={cell} key={key}/> 
        })}
    </tr>
    )
}

const TableCell = ({cell, key}) => {
    return <td key={key}>{cell}</td>
}