import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { GameListComponent } from './game-list/game-list.component';
import { NewGameComponent } from './new-game/new-game.component';
import { ProfileComponent } from './profile/profile.component';
import { ScoreBoardComponent } from './score-board/score-board.component';

const routes: Routes = [
  { path: '', component: GameListComponent },
  { path: 'create', component: NewGameComponent },
  { path: 'profile/:user_id', component: ProfileComponent },
  { path: 'score-board', component: ScoreBoardComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
