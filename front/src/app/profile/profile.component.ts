import { Component, OnInit } from '@angular/core';
import { UserProfile } from '../models/user.model';
import { UserService } from '../services/user.service';
import {ActivatedRoute} from '@angular/router';
import { Observable } from 'rxjs';
import { Store, select } from '@ngrx/store';
import { AuthState } from '../auth/auth.states';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss', '../app.component.scss']
})
export class ProfileComponent implements OnInit {

  profile$!: Observable<UserProfile>;
  userRole$!: Observable<string>;
  userRole!: string;
  userId$!: Observable<number>;
  userId!: number;

  constructor(private userService: UserService, private route: ActivatedRoute, private store: Store<{ auth: AuthState }>) { }

  ngOnInit(): void {
     let user_id: number = this.route.snapshot.params['user_id'];
     this.profile$ = this.userService.getUsersProfile(user_id);

     this.userRole$ = this.store.pipe(select(state => state.auth.role));
     this.userRole$.subscribe(userRole => {
        this.userRole = userRole;
     });

     this.userId$ = this.store.pipe(select(state => state.auth.id));
     this.userId$.subscribe(userId => {
        this.userId = userId;
     });
  }

  canUpdate(profile: UserProfile): boolean {
    return this.userRole == 'admin' || this.userId == profile.id;
  }

  onContentChanged(userId: number, newDisplayName: string) {
      this.userService.modifyDisplayName(userId, newDisplayName).subscribe(
        (data) => console.log("display name updated"),
        (error) => console.log("error")
      );
  }

}
