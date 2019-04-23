export default function publicationReducer(state={
    publicationDetails: {}
}, action) {
    switch(action.type) {
        case "PUBLICATION_SEARCH":
            return {...state, publicationDetails: action.payload.publicationDetails}
    }
    return state
}