import { Component, Input } from '@angular/core';
import { Game } from '../models/game.model';
import { GameService } from '../services/game.service';

@Component({
  selector: 'app-game',
  templateUrl: './game.component.html',
  styleUrls: ['./game.component.scss', '../app.component.scss']
})
export class GameComponent {
  @Input() game!: Game;

  constructor(private gameService: GameService){}

}
