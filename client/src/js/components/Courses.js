import React from "react"
import { connect } from "react-redux"

import { searchCourses } from "../actions/courseSearchAction"
import { fuzzySearchResearcher } from "../actions/fuzzySearchAction";
import NavBar from "./NavBar";

import { Redirect } from "react-router-dom"
@connect((store) => {
    return {
        courseDetails: store["courseReducer"].courseDetails,
        researcherName: store["searchReducer"].researcherName,
        fuzzySearchPattern: store["searchReducer"].fuzzySearchPattern,
        fuzzySearchResults: store["searchReducer"].fuzzySearchResults,
    }
})

export default class Courses extends React.Component {
    constructor(props) {
        super(props);
        this.buttons = {
            'ai': 0,
            'vision': 0,
            'ml': 0,
            'nlp': 0,
            'ir': 0
        }
        this.headers = ["Course Title", "Course Level", "Course Meta", "Units", "Semester", "CourseID", "Grading Method"]
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
            this.props.dispatch(searchCourses(payload));
        } else {
            console.log("No radio button selected");
        }
    }

    render() {
        var { fuzzySearchResults, courseDetails } = this.props;
        var headers = this.headers;
        return (
            <div>
                {/* <NavBar /> */}
                <h1>Courses List page</h1>
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
                    Object.keys(courseDetails).length === 0 && courseDetails.constructor === Object ?
                        (<div id="courseDetails">Empty Publications</div>)
                        : (<CourseDetailsComponent courseDetails={courseDetails.slice(0, 50)} headers={headers} />)
                }

            </div>

        )
    }
}

function CourseDetailsComponent(props) {

    return (
        <div id="courseDetails">

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
                    {props.courseDetails.map((row, key) => {
                        return <TableRow row={row} key={key} />
                    })}
                </tbody>
            </table>
        </div>
    )
}

const TableRow = ({ row, key }) => {
    console.log(row);
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
    console.log(cell, key);
    return <th key={key}>{cell}</th>
}