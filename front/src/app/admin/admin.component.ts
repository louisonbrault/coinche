import { AuthState } from '../auth/auth.states';
import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { Store, select } from '@ngrx/store';
import { UserLight } from '../models/user.model';
import { UserService } from '../services/user.service';
import { NzNotificationPlacement, NzNotificationService } from 'ng-zorro-antd/notification';

@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.scss', '../app.component.scss']
})
export class AdminComponent implements OnInit {

  userRole$!: Observable<string>;
  userRole!: string;

  users$!: Observable<UserLight[]>;

  constructor(private userService: UserService, private store: Store<{ auth: AuthState }>, private notification: NzNotificationService) { }

  ngOnInit(): void {
     this.userRole$ = this.store.pipe(select(state => state.auth.role));
     this.userRole$.subscribe(userRole => {
        this.userRole = userRole;
     });

     this.users$ = this.userService.getAllUsers();

  }

  changeRole(userId: number, role: string): void {
    this.userService.modifyRole(userId, role).subscribe(
        (data) => console.log("role updated"),
        (error) => console.log("error")
      );
  }

  deleteUser(userId: number): void {
    this.userService.deleteUser(userId).subscribe(
        (data) => this.users$ = this.userService.getAllUsers(),
        (error) => {
          this.notification.error(
            "Suppression impossible",
            "L'utilisateur a des parties",
            { nzPlacement: 'bottom' }
          );
        }
      );
  }

}
