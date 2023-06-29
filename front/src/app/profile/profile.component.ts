import { Component, OnInit } from '@angular/core';
import { UserProfile } from '../models/user.model';
import { UserService } from '../services/user.service';
import {ActivatedRoute} from '@angular/router';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss', '../app.component.scss']
})
export class ProfileComponent implements OnInit {

  profile$!: Observable<UserProfile>;

  constructor(private userService: UserService, private route: ActivatedRoute) { }

  ngOnInit(): void {
     let user_id: number = this.route.snapshot.params['user_id'];
     this.profile$ = this.userService.getUsersProfile(user_id);
  }

}
