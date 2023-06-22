import { Component, Input } from '@angular/core';
import { Game } from '../models/game.model';
import { GameService } from '../services/game.service';

@Component({
  selector: 'app-game',
  templateUrl: './game.component.html',
  styleUrls: ['./game.component.scss']
})
export class GameComponent {
  @Input() game!: Game;

  constructor(private gameService: GameService){}


  /**
  ngOnInit() {
    this.date = new Date();
    this.player_a1_name = "Louison";
    this.player_a2 = "Arthur";
    this.player_b1 = "Gaetan";
    this.player_b2 = "Jean";
    this.score_a = 2340;
    this.score_b = 150;
    this.stars_a = Array(1).fill(0).map((x,i)=>i);
    this.stars_b = Array(2).fill(0).map((x,i)=>i);
    this.a_won = true;
    this.b_won = false;
  }
  **/
}
