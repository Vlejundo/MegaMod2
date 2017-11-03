     #### Treasury gold 
     (try_begin),
        (gt, "$g_player_chamberlain", 0),
        (store_troop_gold, ":player_wealth", "trp_household_possessions"),
     (else_try),
      	(store_troop_gold, ":player_wealth", "trp_player"),
     (try_end),