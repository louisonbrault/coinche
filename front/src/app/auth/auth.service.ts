import { Injectable } from '@angular/core';
import { Auth } from '../models/auth.model';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private http: HttpClient){

  }

  login(authToken: string): Observable<Auth> {
      const body = {
        authToken: authToken
      };
      return this.http.post<Auth>('http://localhost:8000/login', body);
  }


}
