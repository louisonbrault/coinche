import { Component, OnInit } from '@angular/core';
import { Game } from '../models/game.model';
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

  games$!: Observable<Game[]>;
  userLoggedIn$!: Observable<boolean>;
  userLoggedIn!: Boolean;
  userRole$!: Observable<string>;
  userRole!: string;

  constructor(
  private gameService: GameService, private store: Store<{ auth: AuthState }>) {}

  ngOnInit(): void {
    this.games$ = this.gameService.getAllGames(0, 3);
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
