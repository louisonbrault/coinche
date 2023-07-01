import { Component, OnInit } from '@angular/core';
import { FacebookLoginProvider, GoogleSigninButtonDirective, SocialAuthService, SocialUser } from "@abacritt/angularx-social-login";
import { Observable } from 'rxjs';
import { Auth } from '../models/auth.model';
import { AuthService } from '../auth/auth.service';
import ls from 'localstorage-slim';
import jwt_decode from 'jwt-decode';

import { Store } from '@ngrx/store';
import { setUserLoggedIn } from '../auth/auth.actions';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {

  user?: SocialUser;
  userId?: number;
  loggedIn!: boolean;

  constructor(
    private socialAuthService: SocialAuthService,
    private authService: AuthService,
    private store: Store) { }

  ngOnInit(): void {
    this.checkIfUserIsAlreadyLoggedIn();

    this.socialAuthService.authState.subscribe((user) => {
        this.user = user;
        if (user){
            this.loginBackend(user);
        }
        this.loggedIn = (user != null);
      });
  }

  signOut(): void {
     this.socialAuthService.signOut().catch(function(error) {
       void(0);
     });
     this.logoutBackend();
  }

  loginBackend(user: SocialUser): void {
    this.authService.login(user.idToken).subscribe(
    (payload: Auth) => {
      ls.set('access_token', payload.access_token, { ttl: payload.expires });
      ls.set('user_photo_url', user.photoUrl, { ttl: payload.expires });
      this.store.dispatch(setUserLoggedIn({ isLoggedIn: user != null, role: this.getUserRole(payload.access_token) }));
      this.userId = this.getUserId(payload.access_token);
    },
    err => this.signOut()
    );
  }

  logoutBackend(): void {
     this.loggedIn = false;
     ls.clear();
     this.store.dispatch(setUserLoggedIn({ isLoggedIn: false, role: "" }));
  }

  checkIfUserIsAlreadyLoggedIn(): void {
     var access_token: string | null = ls.get('access_token');
     if (!access_token){
       return;
     }
     var response = {picture: {data: {url: ls.get('user_photo_url')}}}
     this.user = new SocialUser();
     this.user.photoUrl = ls.get('user_photo_url') || "";
     this.loggedIn = true;
     this.store.dispatch(setUserLoggedIn({ isLoggedIn: true, role: this.getUserRole(access_token) }));
     this.userId = this.getUserId(access_token);
  }

  getUserRole(access_token: string): string {
    var tokenInfo : {role: string, expires: number, user_id: number} = jwt_decode(access_token);
    return tokenInfo.role;
  }

  getUserId(access_token: string): number {
    var tokenInfo : {role: string, expires: number, user_id: number} = jwt_decode(access_token);
    return tokenInfo.user_id;
  }

}
