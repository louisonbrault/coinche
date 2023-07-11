import { Component, OnInit } from '@angular/core';
import { GamesResponse } from '../models/game.model';
import { GameService } from '../services/game.service';
import { Observable } from 'rxjs';
import { Store, select } from '@ngrx/store';
import { AuthState } from '../auth/auth.states';
import ls from 'localstorage-slim';

@Component({
  selector: 'app-game-list',
  templateUrl: './game-list.component.html',
  styleUrls: ['./game-list.component.scss', '../app.component.scss']
})
export class GameListComponent {

  gamesResponse$!: Observable<GamesResponse>;
  userLoggedInId$!: Observable<number>;
  userLoggedInId!: number;

  onlyMyGames: Boolean = false;
  onlyMyCreatedGames: Boolean = false;

  currentPage: number = 1;

  constructor(
    private gameService: GameService,
    private store: Store<{ auth: AuthState }>) {}

  ngOnInit(): void {
    this.gamesResponse$ = this.gameService.getAllGames(1, 4);
    this.userLoggedInId$ = this.store.pipe(select(state => state.auth.id));
    this.userLoggedInId$.subscribe(id => {
      this.userLoggedInId = id;
    });
  }

  onMyGamesChange(){
    this.updateGameList();
  }

  onPageChange(index: number){
    this.currentPage = index;
    this.updateGameList();
  }

  updateGameList(){
    if (this.onlyMyGames && this.onlyMyCreatedGames){
      this.gamesResponse$ = this.gameService.getAllGames(this.currentPage, 4, {userId: this.userLoggedInId, creatorId: this.userLoggedInId});
    }
    if (this.onlyMyGames){
      this.gamesResponse$ = this.gameService.getAllGames(this.currentPage, 4, {userId: this.userLoggedInId});
    }
    if (this.onlyMyCreatedGames){
      this.gamesResponse$ = this.gameService.getAllGames(this.currentPage, 4, {creatorId: this.userLoggedInId});
    }
    if (!this.onlyMyGames && !this.onlyMyCreatedGames){
      this.gamesResponse$ = this.gameService.getAllGames(this.currentPage, 4);
    }
  }

}
