import { Component, OnInit } from '@angular/core';
import { GamesResponse } from '../models/game.model';
import { GameService } from '../services/game.service';
import { Observable } from 'rxjs';
import { ActivatedRoute, Router } from '@angular/router';
import { Store, select } from '@ngrx/store';
import { AuthState } from '../auth/auth.states';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  gamesResponse$!: Observable<GamesResponse>;
  userLoggedInId$!: Observable<number>;
  userLoggedInId!: number;
  userRole$!: Observable<string>;
  userRole!: string;

  constructor(
  private gameService: GameService, private store: Store<{ auth: AuthState }>) {}

  ngOnInit(): void {
    this.gamesResponse$ = this.gameService.getAllGames(1, 3);
    this.userLoggedInId$ = this.store.pipe(select(state => state.auth.id));
    this.userLoggedInId$.subscribe(id => {
      this.userLoggedInId = id;
    });

    this.userRole$ = this.store.pipe(select(state => state.auth.role));
    this.userRole$.subscribe(userRole => {
      this.userRole = userRole;
    });
  }

}
