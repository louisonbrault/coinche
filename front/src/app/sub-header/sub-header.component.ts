import { Component, OnInit } from '@angular/core';
import { Location } from '@angular/common';

@Component({
  selector: 'app-sub-header',
  templateUrl: './sub-header.component.html',
  styleUrls: ['./sub-header.component.scss', '../app.component.scss']
})
export class SubHeaderComponent implements OnInit {

  homeActive!: boolean;
  scoreActive!: boolean;
  gamesActive!: boolean;
  rulesActive!: boolean;

  constructor(private location: Location) { }

  ngOnInit(): void {
    this.homeActive = this.location.path() == "" || this.location.path() == "/" || this.location.path() == "/create";
    this.scoreActive = this.location.path() == "/score-board";
    this.gamesActive = this.location.path() == "/games";
    this.rulesActive = this.location.path() == "/rules";
  }

}
