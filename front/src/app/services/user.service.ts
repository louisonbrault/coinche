import { Injectable } from '@angular/core';
import { UserLight, UserProfile, UserStat } from '../models/user.model';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';


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


}
