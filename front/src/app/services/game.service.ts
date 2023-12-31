import { DatePipe } from '@angular/common';
import { Injectable } from '@angular/core';
import { Game, GamesResponse } from '../models/game.model';
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

  getAllGames(page: number, size: number, options?: {userId?: number, creatorId?: number}): Observable<GamesResponse> {
      var filterString = "";
      if (typeof options !== 'undefined' && typeof options.userId !== 'undefined') {
        filterString += `&user_id=${options.userId}`;
      }
      if (typeof options !== 'undefined' && typeof options.creatorId !== 'undefined') {
        filterString += `&creator_id=${options.creatorId}`;
      }
      return this.http.get<GamesResponse>(`${this.apiUrl}/games?page=${page}&size=${size}${filterString}`);
  }

  getGame(id: number): Observable<Game> {
    return this.http.get<Game>(`${this.apiUrl}/games/${id}`);
  }

  deleteGame(id: number): Observable<void> {
    var access_token = ls.get('access_token');
    const headers = new HttpHeaders({
        'Authorization': `Bearer ${access_token}`
    });
    return this.http.delete<void>(`${this.apiUrl}/games/${id}`, {headers: headers});
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

  modifyGame(
    id: number,
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
    return this.http.put<Game>(`${this.apiUrl}/games/${id}`, postData, {headers: headers});
  }


}
