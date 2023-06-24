import { Injectable } from '@angular/core';
import { Auth } from '../models/auth.model';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';


@Injectable({
  providedIn: 'root'
})
export class AuthService {

  apiUrl = environment.apiUrl;

  constructor(private http: HttpClient){

  }

  login(authToken: string): Observable<Auth> {
      const body = {
        authToken: authToken
      };
      return this.http.post<Auth>(`${this.apiUrl}/login`, body);
  }


}
