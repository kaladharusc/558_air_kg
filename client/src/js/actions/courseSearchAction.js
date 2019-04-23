import axios from "axios";

export function searchCourses(payload) {
    return function(dispatch) {
        var headers = {
            'Content-Type': 'application/json; charset=utf-8',
        }
        var data = {searchQueryParams: payload.searchQueryParams}

        var server_url = "http://localhost:3000/searchCourses";

        axios.post(server_url, data, {headers:headers})
            .then((response) => {
                console.log(response.data);
                dispatch({
                    type: "COURSE_SEARCH",
                    payload: {
                        courseDetails: response.data.msg
                    }
                })
            }).catch((error) => {
                console.log("Error in Course Search");
            })
    }    
}