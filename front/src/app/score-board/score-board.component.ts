import { Component, OnInit } from '@angular/core';
import { UserService } from '../services/user.service';
import { UserStat } from '../models/user.model';
import { Observable } from 'rxjs';
import { NzTableSortFn, NzTableSortOrder } from 'ng-zorro-antd/table';


interface ColumnItem {
  name: string;
  sortOrder: NzTableSortOrder | null;
  sortFn: NzTableSortFn<UserStat> | null;
  sortDirections: NzTableSortOrder[];
}

@Component({
  selector: 'app-score-board',
  templateUrl: './score-board.component.html',
  styleUrls: ['./score-board.component.scss', '../app.component.scss']
})
export class ScoreBoardComponent implements OnInit {

  stats!: UserStat[];
  listOfColumns: ColumnItem[] = [
    {
      name: 'Nom',
      sortOrder: null,
      sortFn: (a: UserStat, b: UserStat) => a.display_name.localeCompare(b.display_name),
      sortDirections: ['ascend', 'descend', null]
    },
    {
      name: 'Parties',
      sortOrder: 'descend',
      sortFn: (a: UserStat, b: UserStat) => a.games - b.games,
      sortDirections: ['ascend', 'descend', null]
    },
    {
      name: 'Ratio',
      sortOrder: null,
      sortDirections: ['ascend', 'descend', null],
      sortFn: (a: UserStat, b: UserStat) => (a.wins/a.games) - (b.wins/b.games)
    },
    {
      name: '⭐️/prt.',
      sortOrder: null,
      sortDirections: ['ascend', 'descend', null],
      sortFn: (a: UserStat, b: UserStat) => (a.stars/a.games) - (b.stars/b.games)
    }
  ];

  constructor(private userService: UserService) { }

  ngOnInit(): void {
    this.userService.getUsersStats().subscribe(
      (data) => this.stats = data,
    );
  }

}
