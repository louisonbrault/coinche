export class UserLight {
    id!: number
    display_name!: string
}

export class UserStat {
    id!: number
    display_name!: string
    games!: number
    wins!: number
    stars!: number
}

export class UserProfile extends UserStat{
    best_teammate!: string
    teammate_times!: number
    best_opponent!: string
    oppositions!: number
    best_target!: string
    victories!: number
    executioner!: string
    defeats!: number
}
