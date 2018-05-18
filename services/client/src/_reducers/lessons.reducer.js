import { lessonConstants } from '../_constants';

const initialState = {
  loading: false,
  error: null,
  items: []
}

export function lessons(state = initialState, action) {
  switch (action.type) {
    case lessonConstants.LESSONS_REQUEST:
      return {
        loading: true,
      };

    case lessonConstants.LESSONS_SUCCESS:
      return {
        ...state,
        loading: false,
        items: [...state.items || [], ...action.items]
      }

    case lessonConstants.LESSONS_FAILURE:
      return {
        loading: false,
        error: action.error
      }

    default:
      return state;


  }
}
