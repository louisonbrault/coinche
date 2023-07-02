import { Component, OnInit } from '@angular/core';
import { GamesResponse } from '../models/game.model';
import { GameService } from '../services/game.service';
import { Observable } from 'rxjs';
import { ActivatedRoute, Router } from '@angular/router';
import { Store, select } from '@ngrx/store';
import { AuthState } from '../auth/auth.states';

@Component({
  selector: 'app-game-list',
  templateUrl: './game-list.component.html',
  styleUrls: ['./game-list.component.scss']
})
export class GameListComponent implements OnInit {

  gamesResponse$!: Observable<GamesResponse>;
  userLoggedIn$!: Observable<boolean>;
  userLoggedIn!: Boolean;
  userRole$!: Observable<string>;
  userRole!: string;

  constructor(
  private gameService: GameService, private store: Store<{ auth: AuthState }>) {}

  ngOnInit(): void {
    this.gamesResponse$ = this.gameService.getAllGames(1, 3);
    this.userLoggedIn$ = this.store.pipe(select(state => state.auth.userLoggedIn));
    this.userLoggedIn$.subscribe(userLoggedIn => {
      this.userLoggedIn = userLoggedIn;
    });

    this.userRole$ = this.store.pipe(select(state => state.auth.role));
    this.userRole$.subscribe(userRole => {
      this.userRole = userRole;
    });
  }

}
