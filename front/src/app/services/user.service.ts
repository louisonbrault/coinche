import { Injectable } from '@angular/core';
import { UserLight, UserProfile, UserStat } from '../models/user.model';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import ls from 'localstorage-slim';


@Injectable({
  providedIn: 'root'
})
export class UserService {

  apiUrl = environment.apiUrl;

  constructor(private http: HttpClient){

  }

  getAllUsers(): Observable<UserLight[]> {
      return this.http.get<UserLight[]>(`${this.apiUrl}/users`);
  }

  getUsersStats(): Observable<UserStat[]> {
      return this.http.get<UserStat[]>(`${this.apiUrl}/stats`);
  }

  getUsersProfile(user_id: number): Observable<UserProfile> {
      return this.http.get<UserProfile>(`${this.apiUrl}/users/${user_id}`);
  }

  modifyDisplayName(user_id: number, display_name: string): Observable<UserLight>{
      var access_token = ls.get('access_token');
      const headers = new HttpHeaders({
          'Authorization': `Bearer ${access_token}`
        });
      return this.http.put<UserLight>(`${this.apiUrl}/users/${user_id}`, {display_name: display_name}, {headers: headers});
  }

  createUser(displayName: string): Observable<UserLight>{
      var access_token = ls.get('access_token');
      const headers = new HttpHeaders({
          'Authorization': `Bearer ${access_token}`
        });
      return this.http.post<UserLight>(`${this.apiUrl}/users`, {display_name: displayName}, {headers: headers});
  }

  modifyRole(user_id: number, role: string): Observable<UserLight>{
      var access_token = ls.get('access_token');
      const headers = new HttpHeaders({
          'Authorization': `Bearer ${access_token}`
        });
      return this.http.put<UserLight>(`${this.apiUrl}/users/${user_id}`, {role: role}, {headers: headers});
  }

  modifyGoogleId(user_id: number, googleId: string): Observable<UserLight>{
      var access_token = ls.get('access_token');
      const headers = new HttpHeaders({
          'Authorization': `Bearer ${access_token}`
        });
      return this.http.put<UserLight>(`${this.apiUrl}/users/${user_id}`, {google_id: googleId}, {headers: headers});
  }

  deleteUser(user_id: number): Observable<void>{
      var access_token = ls.get('access_token');
      const headers = new HttpHeaders({
          'Authorization': `Bearer ${access_token}`
        });
      return this.http.delete<void>(`${this.apiUrl}/users/${user_id}`, {headers: headers});
  }


}
