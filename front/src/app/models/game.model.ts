import { UserLight } from "./user.model";

export class Game {
    id!: number
    date!: Date
    creator!: number
    player_a1!: UserLight
    player_a2!: UserLight
    player_b1!: UserLight
    player_b2!: UserLight
    score_a!: number
    score_b!: number
    stars_a!: number
    stars_b!: number
    a_won!: Boolean
    b_won!: Boolean
}

export class GamesResponse {
  total!: number
  page!: number
  size!: number
  pages!: number
  items!: [Game]
}
