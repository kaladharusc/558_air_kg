import axios from "axios";
import {setCookie, removeCookie} from 'redux-cookie'

export function searchResearcher(payload) {
    return function(dispatch) {
        var headers = {
            'Content-Type': 'application/json; charset=utf-8',
        }
        var data = {searchName: payload.researcherName};
        var serverUrl = "http://localhost:3000/searchDoc";

        axios.post(serverUrl, data, {headers: headers})
            .then((response) => {
                dispatch({
                    type: "SEARCH",
                    payload: {
                        researcherName: payload.researcherName,
                        researcherDetails: response.data.msg
                    }
                })
            }).catch((error) => {
                console.log("Error in Search Doc");
            })
    }
}