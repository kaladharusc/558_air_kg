export default function publicationReducer(state={
    courseDetails: {}
}, action) {
    switch(action.type) {
        case "COURSE_SEARCH":
            return {...state, courseDetails: action.payload.courseDetails}
    }
    return state
}