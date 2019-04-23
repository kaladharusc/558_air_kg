import axios from "axios";
import {setCookie, removeCookie} from 'redux-cookie'

export function searchResearcher(payload) {
    return function(dispatch) {

        dispatch({
            type: "SEARCH",
            payload: payload.researcherName
        });

        // dispatch({type : "LOGGING_IN"})

        // axios.post("http://localhost:8000/api/users/login", payload)
        //     .then((response) => {
        //         dispatch({
        //             type : "LOGGED_IN",
        //             payload : response.data.user
        //         })
        //         dispatch(setCookie('token', "Token "+response.data.user.token))
        //         dispatch(setCookie('user_id', response.data.user._id))
        //         dispatch(setCookie('user_name', response.data.user.email))

        //     })
        //     .catch((err) => {
        //         dispatch({type: "LOGIN_FAILED", payload: err})
        //       })

    }
}