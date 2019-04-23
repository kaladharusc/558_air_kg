export default function searchReducer(state = {
    loggingIn : false,
    loggedIn : false,
    user : {}
}, action) {
    switch (action.type) {
        case "SEARCH" :
            return {...state, researcherName: action.payload}
    }
    return state
}