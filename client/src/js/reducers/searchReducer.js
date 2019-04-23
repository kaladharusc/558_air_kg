export default function searchReducer(state = {
    researcherName: ""
}, action) {
    switch (action.type) {
        case "SEARCH" :
            return {...state, researcherName: action.payload}
    }
    return state
}