import axios from "axios";

export function fuzzySearchResearcher(payload) {
    return function(dispatch) {
        var headers = {
            'Content-Type': 'application/json; charset=utf-8',
        }
        var data = {searchPattern: payload.fuzzySearchPattern}
        axios.post("http://localhost:3000/fuzzySearch", data, {headers: headers})
            .then((response) => {
                dispatch({
                    type: "FUZZY_SEARCH",
                    payload: {
                        fuzzySearchPattern: payload.fuzzySearchPattern,
                        fuzzySearchResults: response.data.msg
                    }
                })
            }).catch((error) => {
                console.log("Error in fuzzySearch");
            })

    }
}