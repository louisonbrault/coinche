import { Component, OnInit } from '@angular/core';
import { Location } from '@angular/common';

@Component({
  selector: 'app-sub-header',
  templateUrl: './sub-header.component.html',
  styleUrls: ['./sub-header.component.scss']
})
export class SubHeaderComponent implements OnInit {

  homeActive!: boolean;
  scoreActive!: boolean;
  historyActive!: boolean;
  rulesActive!: boolean;

  constructor(private location: Location) { }

  ngOnInit(): void {
    this.homeActive = this.location.path() == "" || this.location.path() == "/" || this.location.path() == "/create";
    this.scoreActive = this.location.path() == "/score-board";
    this.historyActive = this.location.path() == "/history";
    this.rulesActive = this.location.path() == "/rules";
  }

}
