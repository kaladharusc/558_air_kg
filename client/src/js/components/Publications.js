import React from "react"
import { connect } from "react-redux"

import { searchPublications } from "../actions/publicationSearchAction"
import { fuzzySearchResearcher } from "../actions/fuzzySearchAction";
import { searchResearcher } from "../actions/searchAction"
import NavBar from "./NavBar";

import { Redirect } from "react-router-dom"
@connect((store) => {
    return {
        publicationDetails: store["publicationReducer"].publicationDetails,
        researcherName: store["searchReducer"].researcherName,
        fuzzySearchPattern: store["searchReducer"].fuzzySearchPattern,
        fuzzySearchResults: store["searchReducer"].fuzzySearchResults,
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
        this.headers = [
            "Co-Authors",
            "Title",
            "url"
        ]
    }

    handleChange(event) {

        if (event.target.name === "fuzzySearchPattern") {
            this[event.target.name] = event.target.value;
            var payload = {
                "fuzzySearchPattern": this.fuzzySearchPattern
            }

            this.props.dispatch(fuzzySearchResearcher(payload));
        } else {
            this.buttons[event.target.value] = this.buttons[event.target.value] ^ 1;
        }
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
                "searchQueryParams": searchQueryParams,
                "researcherName": this.fuzzySearchPattern
            }
            this.props.dispatch(searchPublications(payload));
        } else {
            console.log("No radio button selected");
        }
    }

    render() {
        var { fuzzySearchResults, publicationDetails } = this.props;
        var headers = this.headers;
        return (
            <div>
                {/* <NavBar/> */}
                <h1>Publications List page</h1>
                <div className="select-options">
                    <span><input type="checkbox" onChange={this.handleChange.bind(this)} value="ai" /> AI</span>
                    <span><input type="checkbox" onChange={this.handleChange.bind(this)} value="vision" /> VISION</span>
                    <span><input type="checkbox" onChange={this.handleChange.bind(this)} value="ml" /> ML AND DATA Mining</span>
                    <span><input type="checkbox" onChange={this.handleChange.bind(this)} value="nlp" /> NLP</span>
                    <span><input type="checkbox" onChange={this.handleChange.bind(this)} value="ir" /> IR</span>
                    <label className="label">Prof Name:   </label>
                    <input className="input" list="data" type="text" name="fuzzySearchPattern" onChange={this.handleChange.bind(this)}></input>
                    <datalist id="data">
                        {fuzzySearchResults.map((item, key) => {
                            return <option key={key} value={item} />
                        })}
                    </datalist>
                </div>

                <button class="btn btn-primary search-button" onClick={this.submitRequest.bind(this)}>Search!</button>

                {
                    Object.keys(publicationDetails).length === 0 && publicationDetails.constructor === Object ?
                        (<div id="publicationDetails">Empty Publications</div>)
                        : (<PublicationDetailsComponent headers={headers} publicationDetails={publicationDetails.slice(0, 50)} />)
                }

            </div>

        )
    }
}

function PublicationDetailsComponent(props) {

    return (
        <div id="courseDetails">
            <br />
            <br />
            {/* <BootstrapTable keyField='id' data={ props.courseDetails } columns={ columns } striped hover condensed/> */}
            <table className="table table-bordered table-hover table-striped" width="100%">
                <thead className="thead-dark">
                    <tr>
                        {props.headers.map((header, index) => {
                            console.log(header, index)
                            return <TableHeader cell={header} key={index} />
                        })}
                    </tr>
                </thead>
                <tbody>
                    {props.publicationDetails.map((row, key) => {
                        return <TableRow row={row} key={key} />
                    })}
                </tbody>
            </table>
        </div>
    )
}

const TableRow = ({ row, key }) => {

    return (
        <tr key={key}>
            {Object.values(row).map((cell, key) => {
                return <TableCell cell={cell} key={key} />
            })}
        </tr>
    )
}

const TableCell = ({ cell, key }) => {
    return <td key={key}>{cell}</td>
}

const TableHeader = ({ cell, key }) => {
    return <th key={key}>{cell}</th>
}