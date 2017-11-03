################ game_script in order:
# chest troop
      (try_for_range, ":town_no", walled_centers_begin, walled_centers_end),
        (store_sub, ":offset", ":town_no", towns_begin),
        (store_add, ":cur_object_no", "trp_town_1_seneschal", ":offset"),
        (party_set_slot,":town_no", slot_town_seneschal, ":cur_object_no"),
      (try_end),
	   # Towns:
      (try_for_range, ":item_no", trade_goods_begin, trade_goods_end),
        (store_sub, ":offset", ":item_no", trade_goods_begin),
        (val_add, ":offset", slot_town_trade_good_prices_begin),
        (try_for_range, ":center_no", centers_begin, centers_end),
          (party_set_slot, ":center_no", ":offset", average_price_factor), #1000
        (try_end),
      (try_end),
      
      (call_script, "script_initialize_trade_routes"),                  #F&B return. We want to expand and include new towns aswell as remove downgraded towns
      (call_script, "script_initialize_sea_trade_routes"), ###Seatrade Marker
      (call_script, "script_initialize_town_arena_info"),
	  
	  # fill_village_bound_centers
      #pass 1: Give one village to each castle
      (try_for_range, ":cur_center", castles_begin, castles_end),
        (assign, ":min_dist", 999999),
        (assign, ":min_dist_village", -1),
        (try_for_range, ":cur_village", villages_begin, villages_end),
          (neg|party_slot_ge, ":cur_village", slot_village_bound_center, 1), #skip villages which are already bound.
          (store_distance_to_party_from_party, ":cur_dist", ":cur_village", ":cur_center"),
          (lt, ":cur_dist", ":min_dist"),
          (assign, ":min_dist", ":cur_dist"),
          (assign, ":min_dist_village", ":cur_village"),
        (try_end),
        (party_set_slot, ":min_dist_village", slot_village_bound_center, ":cur_center"),
        (store_faction_of_party, ":town_faction", ":cur_center"),
        (call_script, "script_give_center_to_faction_aux", ":min_dist_village", ":town_faction"),
      (try_end),
      
      
      #pass 2: Give other villages to closest town.
      (try_for_range, ":cur_village", villages_begin, villages_end),
        (neg|party_slot_ge, ":cur_village", slot_village_bound_center, 1), #skip villages which are already bound.
        (assign, ":min_dist", 999999),
        (assign, ":min_dist_town", -1),
        (try_for_range, ":cur_town", towns_begin, towns_end),
          (store_distance_to_party_from_party, ":cur_dist", ":cur_village", ":cur_town"),
          (lt, ":cur_dist", ":min_dist"),
          (assign, ":min_dist", ":cur_dist"),
          (assign, ":min_dist_town", ":cur_town"),
        (try_end),
        (party_set_slot, ":cur_village", slot_village_bound_center, ":min_dist_town"),
        (store_faction_of_party, ":town_faction", ":min_dist_town"),
        (call_script, "script_give_center_to_faction_aux", ":cur_village", ":town_faction"),
      (try_end),
	  # Towns (loop)
    (try_for_range, ":town_no", towns_begin, towns_end),
        (store_sub, ":offset", ":town_no", towns_begin),
        (party_set_slot,":town_no", slot_party_type, spt_town),
        #(store_add, ":cur_object_no", "trp_town_1_seneschal", ":offset"),
        #(party_set_slot,":town_no", slot_town_seneschal, ":cur_object_no"),
        (store_add, ":cur_object_no", "scn_town_1_center", ":offset"),
        (party_set_slot,":town_no", slot_town_center, ":cur_object_no"),
        (troop_set_slot, ":cur_object_no", slot_trp_is_active, 1),
        (store_add, ":cur_object_no", "scn_town_1_castle", ":offset"),
        (party_set_slot,":town_no", slot_town_castle, ":cur_object_no"),
        (troop_set_slot, ":cur_object_no", slot_trp_is_active, 1),
        (store_add, ":cur_object_no", "scn_town_1_prison", ":offset"),
        (party_set_slot,":town_no", slot_town_prison, ":cur_object_no"),
        (troop_set_slot, ":cur_object_no", slot_trp_is_active, 1),
        (store_add, ":cur_object_no", "scn_town_1_walls", ":offset"),
        (party_set_slot,":town_no", slot_town_walls, ":cur_object_no"),
        (troop_set_slot, ":cur_object_no", slot_trp_is_active, 1),
        (store_add, ":cur_object_no", "scn_town_1_tavern", ":offset"),
        (party_set_slot,":town_no", slot_town_tavern, ":cur_object_no"),
        (troop_set_slot, ":cur_object_no", slot_trp_is_active, 1),
        (store_add, ":cur_object_no", "scn_town_1_store", ":offset"),
        (party_set_slot,":town_no", slot_town_store, ":cur_object_no"),
        (troop_set_slot, ":cur_object_no", slot_trp_is_active, 1),
        (store_add, ":cur_object_no", "scn_town_1_arena", ":offset"),
        (party_set_slot,":town_no", slot_town_arena, ":cur_object_no"),
        (troop_set_slot, ":cur_object_no", slot_trp_is_active, 1),
        (store_add, ":cur_object_no", "scn_town_1_alley", ":offset"),
        (party_set_slot,":town_no", slot_town_alley, ":cur_object_no"),
        (troop_set_slot, ":cur_object_no", slot_trp_is_active, 1),
        (store_add, ":cur_object_no", "trp_town_1_mayor", ":offset"),
        (party_set_slot,":town_no", slot_town_elder, ":cur_object_no"),
        (troop_set_slot, ":cur_object_no", slot_trp_is_active, 1),
        (store_add, ":cur_object_no", "trp_town_1_tavernkeeper", ":offset"),
        (party_set_slot,":town_no", slot_town_tavernkeeper, ":cur_object_no"),
        (troop_set_slot, ":cur_object_no", slot_trp_is_active, 1),
        (store_add, ":cur_object_no", "trp_town_1_weaponsmith", ":offset"),
        (party_set_slot,":town_no", slot_town_weaponsmith, ":cur_object_no"),
        (troop_set_slot, ":cur_object_no", slot_trp_is_active, 1),
        (store_add, ":cur_object_no", "trp_town_1_armorer", ":offset"),
        (party_set_slot,":town_no", slot_town_armorer, ":cur_object_no"),
        (troop_set_slot, ":cur_object_no", slot_trp_is_active, 1),
        (store_add, ":cur_object_no", "trp_town_1_merchant", ":offset"),
        (party_set_slot,":town_no", slot_town_merchant, ":cur_object_no"),
        (troop_set_slot, ":cur_object_no", slot_trp_is_active, 1),
        (store_add, ":cur_object_no", "trp_town_1_horse_merchant", ":offset"),
        (party_set_slot,":town_no", slot_town_horse_merchant, ":cur_object_no"),
        (troop_set_slot, ":cur_object_no", slot_trp_is_active, 1),
        (store_add, ":cur_object_no", "scn_town_1_center", ":offset"),
        (party_set_slot,":town_no", slot_town_center, ":cur_object_no"),
		
		(party_set_slot,":town_no", slot_town_reinforcement_party_template, "pt_center_reinforcements"),

    (try_end),
      
      # Castles
    (try_for_range, ":castle_no", castles_begin, castles_end),
        (store_sub, ":offset", ":castle_no", castles_begin),
        (val_mul, ":offset", 3),
        
        #        (store_add, ":senechal_troop_no", "trp_castle_1_seneschal", ":offset"),
        #        (party_set_slot,":castle_no", slot_town_seneschal, ":senechal_troop_no"),
        (store_add, ":exterior_scene_no", "scn_castle_1_exterior", ":offset"),
        (party_set_slot,":castle_no", slot_castle_exterior, ":exterior_scene_no"),
        (store_add, ":interior_scene_no", "scn_castle_1_interior", ":offset"),
        (party_set_slot,":castle_no", slot_town_castle, ":interior_scene_no"),
        (store_add, ":interior_scene_no", "scn_castle_1_prison", ":offset"),
        (party_set_slot,":castle_no", slot_town_prison, ":interior_scene_no"),
        
		(party_set_slot,":castle_no", slot_town_reinforcement_party_template, "pt_center_reinforcements"),
        (party_set_slot,":castle_no", slot_party_type, spt_castle),
        (party_set_slot,":castle_no", slot_center_is_besieged_by, -1),
		
	(try_end),
	# Set which castles need to be attacked with siege towers.
      (party_set_slot,"p_town_13", slot_center_siege_with_belfry, 1),
      (party_set_slot,"p_town_16", slot_center_siege_with_belfry, 1),
      
      (party_set_slot,"p_castle_1", slot_center_siege_with_belfry, 1),
      (party_set_slot,"p_castle_2", slot_center_siege_with_belfry, 1),
      (party_set_slot,"p_castle_4", slot_center_siege_with_belfry, 1),
      (party_set_slot,"p_castle_7", slot_center_siege_with_belfry, 1),
      (party_set_slot,"p_castle_8", slot_center_siege_with_belfry, 1),
      (party_set_slot,"p_castle_9", slot_center_siege_with_belfry, 1),
      (party_set_slot,"p_castle_11", slot_center_siege_with_belfry, 1),
      (party_set_slot,"p_castle_13", slot_center_siege_with_belfry, 1),
      (party_set_slot,"p_castle_21", slot_center_siege_with_belfry, 1),
      (party_set_slot,"p_castle_25", slot_center_siege_with_belfry, 1),
      (party_set_slot,"p_castle_34", slot_center_siege_with_belfry, 1),
      (party_set_slot,"p_castle_35", slot_center_siege_with_belfry, 1),
      (party_set_slot,"p_castle_38", slot_center_siege_with_belfry, 1),
      (party_set_slot,"p_castle_40", slot_center_siege_with_belfry, 1),
      (party_set_slot,"p_castle_41", slot_center_siege_with_belfry, 1),
      (party_set_slot,"p_castle_42", slot_center_siege_with_belfry, 1),
      (party_set_slot,"p_castle_43", slot_center_siege_with_belfry, 1),
      
      # Villages            #F&B return here for set_scenes 
      (try_for_range, ":village_no", villages_begin, villages_end),
        (store_sub, ":offset", ":village_no", villages_begin),
        
        (store_add, ":exterior_scene_no", "scn_village_1", ":offset"),
        (party_set_slot,":village_no", slot_castle_exterior, ":exterior_scene_no"),
        
        (store_add, ":store_troop_no", "trp_village_1_elder", ":offset"),
        (party_set_slot,":village_no", slot_town_elder, ":store_troop_no"),
        (troop_set_slot, ":store_troop_no", slot_trp_is_active, 1),
        
        (party_set_slot,":village_no", slot_party_type, spt_village),
        (party_set_slot,":village_no", slot_village_raided_by, -1),
        
        (call_script, "script_start_refresh_village_defenders", ":village_no"),
        (call_script, "script_start_refresh_village_defenders", ":village_no"),
        (call_script, "script_start_refresh_village_defenders", ":village_no"),
        (call_script, "script_start_refresh_village_defenders", ":village_no"),
      (try_end),
      
      (try_for_range, ":center_no", centers_begin, centers_end),        #F&B return we might have to include this for new fiefs
        (party_set_slot, ":center_no", slot_center_last_spotted_enemy, -1),
        (party_set_slot, ":center_no", slot_center_is_besieged_by, -1),
        (party_set_slot, ":center_no", slot_center_last_taken_by_troop, -1),
        ##diplomacy start+ Set the home slots for town merchants, elders, etc. for reverse-lookup
        (try_for_range, ":offset", dplmc_slot_town_merchants_begin, dplmc_slot_town_merchants_end),
           (party_get_slot, ":npc", ":center_no", ":offset"),
           (gt, ":npc", 0),
           (neg|troop_slot_ge, ":npc", slot_troop_home, 1),#If the startup script wasn't altered by another mod, we don't have to worry about this condition.
           (troop_set_slot, ":npc", slot_troop_home, ":center_no"),
        (try_end),
        ##diplomacy end+
      (try_end),
	  (try_for_range, ":center_no", centers_begin, centers_end),
        (add_party_note_tableau_mesh, ":center_no", "tableau_center_note_mesh"),
      (try_end),
	  
	  (call_script, "script_give_center_to_faction_aux", "p_town_1", "fac_kingdom_4"),
	  
      (call_script, "script_give_center_to_faction_aux", "p_castle_1", "fac_kingdom_5"),
	  
      (call_script, "script_start_give_center_to_lord", "p_town_1",  "trp_kingdom_4_lord", 0),
	  #set original factions
      (try_for_range, ":center_no", centers_begin, centers_end),
        (store_faction_of_party, ":original_faction", ":center_no"),
        (faction_get_slot, ":culture", ":original_faction", slot_faction_culture),
        (party_set_slot, ":center_no", slot_center_culture,  ":culture"),
        (party_set_slot, ":center_no", slot_center_original_faction,  ":original_faction"),
        (party_set_slot, ":center_no", slot_center_ex_faction,  ":original_faction"),
		##diplomacy start+ set additional slots
		    (party_get_slot, ":town_lord", ":center_no", slot_town_lord),
		
		  (try_begin),
			 (eq, ":town_lord", "trp_player"),
			 #Use trp_kingdom_heroes_including_player_begin instead of trp_player as a workaround for
			 #old saved games (since uninitialized memory is 0).
			 (party_set_slot, ":center_no", dplmc_slot_center_ex_lord, "trp_kingdom_heroes_including_player_begin"),
			 (troop_slot_eq, "trp_player", slot_troop_home, ":center_no"),
			 (neg|party_slot_ge, ":center_no", dplmc_slot_center_original_lord, 1),
			 (party_set_slot, ":center_no", dplmc_slot_center_original_lord, "trp_kingdom_heroes_including_player_begin"),
		  (else_try),
			 (party_set_slot, ":center_no", dplmc_slot_center_ex_lord, ":town_lord"),
			 (ge, ":town_lord", 0),
			 (troop_slot_eq, ":town_lord", slot_troop_home, ":center_no"),
			 (neg|party_slot_ge, ":center_no", dplmc_slot_center_original_lord, 1),
			 (party_set_slot, ":center_no", dplmc_slot_center_original_lord, ":town_lord"),
		  (try_end),
		##diplomacy end+
      (try_end),
	  
      (call_script, "script_update_village_market_towns"),
	  
      #Initialize walkers
      (try_for_range, ":center_no", centers_begin, centers_end),
        (this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
        (party_slot_eq, ":center_no", slot_party_type, spt_village),
        (try_for_range, ":walker_no", 0, num_town_walkers),
          (call_script, "script_center_set_walker_to_type", ":center_no", ":walker_no", walkert_default),
        (try_end),
      (try_end),
	  
	  #This needs to be after market towns
	  (call_script, "script_initialize_economic_information"),

	  (try_for_range, ":village_no", villages_begin, villages_end),
        (call_script, "script_refresh_village_merchant_inventory", ":village_no"),
      (try_end),
	  (try_for_range, ":troop_id", original_kingdom_heroes_begin, active_npcs_end),
        (try_begin),
          (store_troop_faction, ":faction_id", ":troop_id"),
          (is_between, ":faction_id", kingdoms_begin, kingdoms_end),
          (troop_set_slot, ":troop_id", slot_troop_original_faction, ":faction_id"),
          (try_begin),
            (is_between, ":troop_id", pretenders_begin, pretenders_end),
            (faction_set_slot, ":faction_id", slot_faction_has_rebellion_chance, 1),
          (try_end),
        (try_end),
        (assign, ":initial_wealth", 6000),
        (try_begin),
          (store_troop_faction, ":faction", ":troop_id"),
          (faction_slot_eq, ":faction", slot_faction_leader, ":troop_id"),
          (assign, ":initial_wealth", 20000),
        (try_end),
        (troop_set_slot, ":troop_id", slot_troop_wealth, ":initial_wealth"),
      (try_end),

      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),#add town garrisons
        #Add initial center wealth
        (assign, ":initial_wealth", 2000),
        (try_begin),
          (is_between, ":center_no", towns_begin, towns_end),
          (val_mul, ":initial_wealth", 2),
        (try_end),
        (party_set_slot, ":center_no", slot_town_wealth, ":initial_wealth"),

        (assign, ":garrison_strength", 15),
        (try_begin),
          (party_slot_eq, ":center_no", slot_party_type, spt_town),
          (assign, ":garrison_strength", 40),
        (try_end),
        (try_for_range, ":unused", 0, ":garrison_strength"),
          (call_script, "script_cf_reinforce_party", ":center_no"),
        (try_end),
        ## ADD some XP initially
        (store_div, ":xp_rounds", ":garrison_strength", 5),
        (val_add, ":xp_rounds", 2),
        
        (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
        
        (try_begin), #hard
          (eq, ":reduce_campaign_ai", 0),
          (assign, ":xp_addition_for_centers", 7500),
        (else_try), #moderate
          (eq, ":reduce_campaign_ai", 1),
          (assign, ":xp_addition_for_centers", 5000),
        (else_try), #easy
          (eq, ":reduce_campaign_ai", 2),
          (assign, ":xp_addition_for_centers", 2500),
        (try_end),
        
        (try_for_range, ":unused", 0, ":xp_rounds"),
          (party_upgrade_with_xp, ":center_no", ":xp_addition_for_centers", 0),
        (try_end),
        
        #Fill town food stores upto half the limit
        (call_script, "script_center_get_food_store_limit", ":center_no"),
        (assign, ":food_store_limit", reg0),
        (val_div, ":food_store_limit", 2),
        (party_set_slot, ":center_no", slot_party_food_store, ":food_store_limit"),
        
        #create lord parties
        (party_get_slot, ":center_lord", ":center_no", slot_town_lord),
        (ge, ":center_lord", 1),
        (troop_slot_eq, ":center_lord", slot_troop_leaded_party, 0),
		(assign, "$g_there_is_no_avaliable_centers", 0),
        (call_script, "script_create_kingdom_hero_party", ":center_lord", ":center_no"),
        (assign, ":lords_party", "$pout_party"),
        (party_attach_to_party, ":lords_party", ":center_no"),
        (party_set_slot, ":center_no", slot_town_player_odds, 1000),
      (try_end),
	  
	 ##diplomacy start+
     ##Initialize town "last caravan arrived" times randomly
	  (try_for_range, ":cur_town", towns_begin, towns_end),
	     (try_for_range, ":cur_slot", dplmc_slot_town_trade_route_last_arrivals_begin, dplmc_slot_town_trade_route_last_arrivals_end),
		    (party_slot_eq, ":cur_town", ":cur_slot", 0),
		    (store_random_in_range, ":last_arrived", 1, (24 * 7 * 5) + 1),#some time in the last five weeks
			(val_mul, ":last_arrived", -1),			
			(party_get_slot, ":prosperity_factor", ":cur_town", slot_town_prosperity),#modify plus or minus 40% based on prosperity
			(val_clamp, ":prosperity_factor", 0, 101),
			(val_add, ":prosperity_factor", 75),
			(val_mul, ":last_arrived", 125),
			(val_div, ":last_arrived", ":prosperity_factor"),#last arrival some time in the last five weeks, plus or minus 40%
			(party_set_slot, ":cur_town", ":cur_slot", ":last_arrived"),
		 (try_end),
	  (try_end),
      (try_for_range, ":cur_village", villages_begin, villages_end),
          (party_get_slot, ":prosperity_factor", ":cur_town", slot_town_prosperity),#modify plus or minus 40% based on prosperity
          (val_clamp, ":prosperity_factor", 0, 101),
          (val_add, ":prosperity_factor", 75),#average 125, min 75, max 175          
          (store_random_in_range, ":last_arrived", 1, (24 * 7) + 1),
          (val_mul, ":last_arrived", -1),#some time in the last 7 days, plus or minus 40%
          (val_mul, ":last_arrived", 125),
          (val_div, ":last_arrived", ":prosperity_factor"),
          (party_set_slot, ":cur_village", dplmc_slot_village_trade_last_returned_from_market, ":last_arrived"),
          (store_random_in_range, ":last_arrived", 1, (24 * 7) + 1),
          (val_mul, ":last_arrived", -1),#some time in the last 7 days
          (val_mul, ":last_arrived", 125),
          (val_div, ":last_arrived", ":prosperity_factor"),
          (party_set_slot, ":cur_village", dplmc_slot_village_trade_last_arrived_to_market, ":last_arrived"),
      (try_end),
      ##diplomacy end+
	  
      (call_script, "script_update_town_specialists"),	#Floris STAT
      (call_script, "script_update_companion_candidates_in_taverns"),
      (call_script, "script_update_ransom_brokers"),
      (call_script, "script_update_tavern_travellers"),
      (call_script, "script_update_tavern_minstrels"),
      (call_script, "script_update_booksellers"),
	  #Duh Town Population for Land required // Linked to bank system
	  
	  (try_for_range, ":town_no", towns_begin, towns_end),
		(this_or_next|eq,":town_no","p_town_1"),
		(this_or_next|eq,":town_no","p_town_5"),
		(this_or_next|eq,":town_no","p_town_6"),
		(this_or_next|eq,":town_no","p_town_8"),
		(this_or_next|eq,":town_no","p_town_10"),
		(eq,"$current_town","p_town_19"),
		(store_random_in_range, ":amount", 18000, 22000),
		(party_set_slot, ":town_no", slot_center_population, ":amount"),
		(val_div, ":amount", 200),
		(party_set_slot, ":town_no", slot_town_acres, ":amount"),
	  (else_try),
		(store_random_in_range, ":amount", 8000, 12000),
		(party_set_slot, ":town_no", slot_center_population, ":amount"),
		(val_div, ":amount", 200),
		(party_set_slot, ":town_no", slot_town_acres, ":amount"),		
	  (try_end),
	  
	  #Duh Over
	  #TEMPERED    ADDED CALL TO SCRIPT TO INITIALIZE MODULE VARIABLES AND SLOTS
      (call_script, "script_init_temp_var"),