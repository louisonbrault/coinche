import { Component, OnInit } from '@angular/core';
import { UserProfile } from '../models/user.model';
import { UserService } from '../services/user.service';
import {ActivatedRoute} from '@angular/router';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss', '../app.component.scss']
})
export class ProfileComponent implements OnInit {

  profile!: UserProfile;

  constructor(private userService: UserService, private route: ActivatedRoute) { }

  ngOnInit(): void {
     let user_id: number = this.route.snapshot.params['user_id'];
     this.userService.getUsersProfile(user_id).subscribe(
        (data) => this.profile = data,
      );
  }

}
