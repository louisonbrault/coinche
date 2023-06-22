import { Injectable } from '@angular/core';
import { UserLight, UserProfile, UserStat } from '../models/user.model';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class UserService {

  constructor(private http: HttpClient){

  }

  getAllUsers(): Observable<UserLight[]> {
      return this.http.get<UserLight[]>(`http://localhost:8000/users`);
  }

  getUsersStats(): Observable<UserStat[]> {
      return this.http.get<UserStat[]>(`http://localhost:8000/stats`);
  }

  getUsersProfile(user_id: number): Observable<UserProfile> {
      return this.http.get<UserProfile>(`http://localhost:8000/users/${user_id}`);
  }


}
