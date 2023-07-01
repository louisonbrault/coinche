import { createReducer, on } from '@ngrx/store';
import { setUserLoggedIn } from './auth.actions';
import { AuthState } from './auth.states';

const initialState: AuthState = {
  userLoggedIn: false,
  role: "",
  id: 0
};

export const authReducer = createReducer(
  initialState,
  on(setUserLoggedIn, (state, { isLoggedIn, role, id }) => ({ ...state, userLoggedIn: isLoggedIn, role: role, id: id })),
);
