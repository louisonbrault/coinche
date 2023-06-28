import { Component, OnInit } from '@angular/core';
import { UserLight } from '../models/user.model';
import { UserService } from '../services/user.service';
import { GameService } from '../services/game.service';
import { Observable } from 'rxjs';
import { ActivatedRoute, Router } from '@angular/router';
import { AbstractControl, UntypedFormBuilder, UntypedFormGroup, Validators } from '@angular/forms';
import { NzNotificationPlacement, NzNotificationService } from 'ng-zorro-antd/notification';
import { Store, select } from '@ngrx/store';
import { AuthState } from '../auth/auth.states';

@Component({
  selector: 'app-new-game',
  templateUrl: './new-game.component.html',
  styleUrls: ['./new-game.component.scss', '../app.component.scss']
})
export class NewGameComponent implements OnInit {

  users!: UserLight[];
  gameForm!: UntypedFormGroup;
  userLoggedIn$!: Observable<boolean>;
  userLoggedIn!: Boolean;
  userRole$!: Observable<string>;
  userRole!: string;

  constructor(
    private formBuilder: UntypedFormBuilder,
    private userService: UserService,
    private gameService: GameService,
    private route: ActivatedRoute,
    private router: Router,
    private notification: NzNotificationService,
    private store: Store<{ auth: AuthState }>) { }

  ngOnInit(): void {
    this.userService.getAllUsers().subscribe(
      (data) => this.users = data,
    );

    this.gameForm = this.formBuilder.group({
      player_a1_id: [null, Validators.required],
      player_a2_id: [null, Validators.required],
      player_b1_id: [null, Validators.required],
      player_b2_id: [null, Validators.required],
      score_a: [null, Validators.required],
      score_b: [null, Validators.required],
      stars_a: [0, Validators.required],
      stars_b: [0, Validators.required],
      winner: [null, Validators.required],
      date: [new Date(), Validators.required]
    },
    {
      validator: checkPlayerValidator('player_a1_id', 'player_a2_id', 'player_b1_id', 'player_b2_id')
    });

    this.userLoggedIn$ = this.store.pipe(select(state => state.auth.userLoggedIn));
    this.userLoggedIn$.subscribe(userLoggedIn => this.userLoggedIn = userLoggedIn);

    this.userRole$ = this.store.pipe(select(state => state.auth.role));
    this.userRole$.subscribe(userRole => this.userRole = userRole);
  }

  onSubmitForm(){
    if (this.gameForm.valid) {
      this.gameService.addGame(this.gameForm.value).subscribe(
      (data) => this.router.navigateByUrl(""),
      (error) => {
          if(error.status == 422){
            sendErrorMessage(this.notification, "VALIDATION_ERROR");
          } else {
            sendErrorMessage(this.notification, "SERVER_ERROR");
          }
      }
    );
    } else {
      sendErrorMessage(this.notification, "FORM_ERROR");
      Object.values(this.gameForm.controls).forEach(control => {
        if (control.invalid) {
          control.markAsDirty();
          control.updateValueAndValidity({ onlySelf: true });
        }
      });
    }
  }
}

export function checkPlayerValidator(field1: string, field2: string, field3: string, field4: string) {
  return function (frm: any) {
    let field1Value = frm.get(field1).value;
    let field2Value = frm.get(field2).value;
    let field3Value = frm.get(field3).value;
    let field4Value = frm.get(field4).value;

    let fields = [field1Value, field2Value, field3Value, field4Value];
    let fieldsSet = new Set(fields);

    if (fields.length != fieldsSet.size) {
      return { 'match': "Players should be differents" }
    }
    return null;
  }
}

export function sendErrorMessage(notification: NzNotificationService, errorType: string){
  console.log(errorType);
  switch(errorType) {
   case "FORM_ERROR": {
      notification.error(
        "Impossible de créer la partie",
        "Vérifie que les joueurs sont différents, que le score et correct et que tu as coché une équipe gagnante",
        { nzPlacement: 'bottom' }
      );
      break;
   }
   case "VALIDATION_ERROR": {
      notification.error(
        "Impossible de créer la partie",
        "Vérifie que le score et les étoiles sont correctes",
        { nzPlacement: 'bottom' }
      );
      break;
   }
   case "SERVER_ERROR": {
      notification.error(
        "Impossible de créer la partie",
        "Problème serveur 💣",
        { nzPlacement: 'bottom' }
      );
      break;
   }
  }
}
