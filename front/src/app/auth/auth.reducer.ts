import { createReducer, on } from '@ngrx/store';
import { setUserLoggedIn } from './auth.actions';
import { AuthState } from './auth.states';

const initialState: AuthState = {
  userLoggedIn: false,
  role: ""
};

export const authReducer = createReducer(
  initialState,
  on(setUserLoggedIn, (state, { isLoggedIn, role }) => ({ ...state, userLoggedIn: isLoggedIn, role: role })),
);
