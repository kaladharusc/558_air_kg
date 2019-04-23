export default function searchReducer(state = {
    researcherName: "",
    fuzzySearchPattern: "",
    fuzzySearchResults: [],
    researcherDetails: {}
}, action) {
    switch (action.type) {
        case "SEARCH" :
            return {...state, researcherName: action.payload.researcherName, 
                researcherDetails: action.payload.researcherDetails}
        case "FUZZY_SEARCH":
            return {...state, fuzzySearchPattern: action.payload.fuzzySearchPattern, 
                fuzzySearchResults: action.payload.fuzzySearchResults}
    }
    return state
}