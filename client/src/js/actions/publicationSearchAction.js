import axios from "axios";

export function searchPublications(payload) {
    return function (dispatch) {
        var headers = {
            'Content-Type': 'application/json; charset=utf-8',
        }
        var data = {
            searchQueryParams: payload.searchQueryParams,
            searchName: payload.researcherName
        }

        var server_url = "http://localhost:3000/searchPublications";

        axios.post(server_url, data, {
                headers: headers
            })
            .then((response) => {
                dispatch({
                    type: "PUBLICATION_SEARCH",
                    payload: {
                        publicationDetails: response.data.msg
                    }
                })
            }).catch((error) => {
                console.log("Error in Publication Search");
            })
    }
}