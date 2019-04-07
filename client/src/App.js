import React, { Component } from 'react';
// import logo from './logo.svg';
import stanford from './data/stanford_corpus.json'
import './App.css';
import 'react-bootstrap-table-next/dist/react-bootstrap-table2.min.css';
import BootstrapTable from 'react-bootstrap-table-next';

console.log(stanford);
const products = stanford['Aaron Sidford']['courses']

const columns = [{
  dataField: 'courseId',
  text: 'Course ID'
}, {
  dataField: 'courseLevel',
  text: 'Course Level'
}, {
  dataField: 'courseMeta',
  text: 'Course Meta'
}, {
  dataField: 'courseTitle',
  text: 'Course Title'
}, {
  dataField: 'gradingMethod',
  text: "Grading Method"
}, {
  dataField: "numberOfUnits",
  text: "Number of Units"
}, {
  dataField: "semester",
  text: "Semester"
}];

class App extends Component {
  constructor(props) {
    super(props);
  }

  componentDidMount() {

  }

  componentDidUpdate() {

  }

  render() {
    return (
      <div>
        <BootstrapTable keyField='id' data={ products } columns={ columns } striped hover condensed/>
      </div>
    );

  }
}
export default App;
