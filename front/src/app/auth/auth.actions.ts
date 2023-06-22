import { createAction, props } from '@ngrx/store';

export const setUserLoggedIn = createAction('[Auth] Set User Logged In', props<{ isLoggedIn: boolean, role: string }>());
