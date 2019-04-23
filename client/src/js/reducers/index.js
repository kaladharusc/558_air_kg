import { combineReducers } from "redux"

import searchReducer from "./searchReducer";
import publicationReducer from "./publicationReducer";
import courseReducer from "./courseReducer";


export default combineReducers({
  searchReducer,
  publicationReducer,
  courseReducer
})
