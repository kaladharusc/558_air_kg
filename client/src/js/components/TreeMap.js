import React from "react"
import { connect } from "react-redux"

import {searchResearcher} from "../actions/searchAction"
import {fuzzySearchResearcher} from "../actions/fuzzySearchAction";
import NavBar from "./NavBar";
import adjancenyList from "../data/adjacency_list.json";
import graphdracula from "graphdracula";

import {Redirect} from "react-router-dom"
@connect((store) => {
    return {
        researcherName: store["searchReducer"].researcherName,
        fuzzySearchPattern: store["searchReducer"].fuzzySearchPattern,
        fuzzySearchResults: store["searchReducer"].fuzzySearchResults,
        researcherDetails: store["searchReducer"].researcherDetails
    }
})

export default class TreeMap extends React.Component {
    constructor(props) {
        super(props);
        // researcherName = "";
        // fuzzySearchPattern = "";
        // fuzzySearchResults = [];
    }

    submitRequest() {
        var visited = []

        var Graph = graphdracula.Graph
        var Renderer = graphdracula.Renderer.Raphael
        var Layout = graphdracula.Layout.Spring

        var graph = new Graph()

        var queue = [];
        queue.push(this.fuzzySearchPattern);
        console.log(queue);

        while(queue.length != 0 && graph.edges.length < 30) {
            console.log(queue);
            let key = queue.shift();
            visited.push(key);
            // queue.push(...adjancenyList[key]);
            if (adjancenyList[key]) {
                adjancenyList[key].forEach(element => {
                    if (!visited.includes(element)) {
                        queue.push(element);
                        graph.addEdge(key, element); 
                    }
                });
            }
        }

        console.log(graph);

        var layout = new Layout(graph)
        var renderer = new Renderer('#paper', graph, 1000, 1000)
        renderer.draw()

    }

    handleChange(event) {
        this[event.target.name] = event.target.value;
        var payload = {
            "fuzzySearchPattern": this.fuzzySearchPattern
        }

        this.props.dispatch(fuzzySearchResearcher(payload));
    }

    render() {
        var {fuzzySearchResults, researcherDetails} = this.props;
        if (Object.keys(researcherDetails).length != 0) {
            console.log(researcherDetails[0]._source);
        }
        return (<div>
            {/* <NavBar/> */}
            <h1>Search Researchers page</h1>
            <input className="input" list="data" type="text" name="fuzzySearchPattern" onChange={this.handleChange.bind(this)}></input>
            <datalist id="data">
                {fuzzySearchResults.map((item, key) => {
                    return <option key={key} value={item} />
                })}
            </datalist>
            <button className="btn btn-dark" onClick={this.submitRequest.bind(this)}>Search!</button>
            
            <div id="paper"></div>

        </div>)
    }
}

function ResearcherDetailsComponent(props) {
    return (
        <div>
            <br/>
            <br/>
            <table className="table table-bordered table-hover" width="100%">
                <tr>
                    <td>
                        Researcher's Name
                    </td>
                    <td>
                        {props.details.person}
                    </td>
                </tr>
                <tr>
                    <td>
                        University Name
                    </td>
                    <td>
                        {props.details.univ_name}
                    </td>
                </tr>
                <tr>
                    <td>
                        Number of papers published
                    </td>
                    <td>
                        {props.details.no_of_papers}
                    </td>
                </tr>
                <tr>
                    <td>
                        Number of courses taught
                    </td>
                    <td>
                        {props.details.courses.length}
                    </td>
                </tr>
                <tr>
                    <td>
                        DBLP
                    </td>
                    <td>
                        {props.details.corpus.DBLP}
                    </td>
                </tr>
                <tr>
                    <td>
                        Google Scholar
                    </td>
                    <td>
                        {props.details.corpus["Google Scholar"]}
                    </td>
                </tr>
                <tr>
                    <td>
                        Domain
                    </td>
                    <td>
                        {props.details.corpus.domain}
                    </td>
                </tr>
                <tr>
                    <td>
                        Home Page
                    </td>
                    <td>
                        {props.details.corpus.home}
                    </td>
                </tr>
            </table>
        </div>

    )
}