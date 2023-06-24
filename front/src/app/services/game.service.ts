import { DatePipe } from '@angular/common';
import { Injectable } from '@angular/core';
import { Game } from '../models/game.model';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import ls from 'localstorage-slim';
import { environment } from 'src/environments/environment';


@Injectable({
  providedIn: 'root'
})
export class GameService {

  apiUrl = environment.apiUrl;

  constructor(private http: HttpClient, private datepipe: DatePipe){

  }

  getAllGames(skip: number, limit: number): Observable<Game[]> {
      return this.http.get<Game[]>(`${this.apiUrl}/games?skip=${skip}&limit=${limit}`);
  }

  addGame(
    formValue:{
      player_a1_id: string,
      player_a2_id: string,
      player_b1_id: string,
      player_b2_id: string,
      score_a: number,
      score_b: number,
      stars_a: number,
      stars_b: number,
      winner: string,
      date: Date
    }
  ): Observable<Game> {
    var postData: any = {
      ...formValue,
      a_won: formValue['winner'] == "A",
      b_won: formValue['winner'] == "B"
    };
    postData["date"] = this.datepipe.transform(postData["date"], 'yyyy-MM-dd');
    delete postData['winner']
    var access_token = ls.get('access_token');
    const headers = new HttpHeaders({
        'Authorization': `Bearer ${access_token}`
      });
    return this.http.post<Game>(`${this.apiUrl}/games`, postData, {headers: headers});
  }


}
