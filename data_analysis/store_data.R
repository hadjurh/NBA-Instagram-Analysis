# Store my data
id <- scan(file = '../database/network_players_gt46_games/ids.txt', what = '', sep = '\n')
player_username_team <- data.frame(NAME=players,
                                   USERNAME=names,
                                   ID=id,
                                   TEAM=teams)
player_username_team$NAME <- player_username_team$NAME %>% unfactor()
player_username_team$USERNAME <- player_username_team$USERNAME %>% unfactor()
player_username_team <- rbind(player_username_team, c("Alex Len", "alexlen_21", "PHX"))
player_username_team <- rbind(player_username_team, c("Yogi Ferrell", "yogiferre11", "DAL"))
player_username_team <- rbind(player_username_team, c("John Wall", "johnwall", "WAS"))
write.csv(player_username_team, file = 'player_username_gt46_games.csv', row.names = FALSE)

