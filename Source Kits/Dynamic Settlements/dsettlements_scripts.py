# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from module_constants import *
from module_constants import *
from header_parties import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from header_map_icons import *
from ID_animations import *
#from header_parties import *    #F&B injected
##diplomacy start+
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin
##diplomacy end+

## CC
from module_my_mod_set import *
from header_presentations import *
## CC

##diplomacy begin
##jrider reports
from header_presentations import tf_left_align
##diplomacy end
from module_party_templates import pf_deserters
from module_constants import *
from dsettlements_constants import *
#from dsettlements_troops import *

scripts = [ 
  #("new_script", [])
	# "script_construct_settlement"
	# Description: Starts construction of a settlement. Puts the construction site on worldmap. Called via script_dynamic_settlements_ai and through game_menus
	# Input: arg1: ":orig_center", arg2: slot_party_type of new center
	# Output: none
	("construct_settlement",
	 [
	  (store_script_param_1, ":orig_center"),
	  (store_script_param_2, ":spt"),

	  (store_faction_of_party, ":faction", ":orig_center"),
	  (party_get_slot, ":town_lord", ":orig_center", slot_town_lord),
	  (party_get_slot, ":prosperity", ":orig_center", slot_town_prosperity),
	  (str_store_party_name, s1, ":orig_center"),
	  (store_time_of_day, ":days"),
	  (party_get_skill_level, ":engi_lvl", "p_main_party", skl_engineer),	
	  
	  (assign, ":time", 60),						#Base construction time is (60 days - engi skill*2)*(settlement multipier)
	  (val_mul, ":engi_lvl", 2),
	  (val_sub, ":time", ":engi_lvl"),

	  (try_begin),
	  	(neq, ":town_lord", "trp_player"),
	  	(set_spawn_radius, 15),
	  	(spawn_around_party, ":orig_center", "pt_construction_site"),
	  (else_try),
	  	(set_spawn_radius, 0),
	  	(spawn_around_party, "p_main_party", "pt_construction_site"),
	  (try_end),
	  (assign, ":new_center", reg0),	  
	  (call_script, "script_name_generator", ":new_center"),

	  (party_set_flags, ":new_center", pf_hide_defenders, -1),
	  (party_set_name, ":new_center", "@Construction site of {reg1}"),
	  (party_set_slot, ":new_center", slot_in_construction, 1),					#This is important, so simple_trigger can track it
	  (party_set_slot, ":new_center", slot_construction_started, ":days"),
	  (party_set_slot, ":new_center", slot_construction_lord, ":town_lord"),
	  (party_set_slot, ":new_center", slot_construction_faction, ":faction"),
	  (party_set_slot, ":new_center", slot_constructing_center, ":orig_center"),
	  (party_set_slot, ":new_center", slot_orig_name, reg1), 

	  (try_begin),
	      (eq, spt_village, ":spt"),
	      (val_mul, ":time", 1),
	      (val_sub, ":prosperity", 20),
	      (val_clamp, ":prosperity", 5, 80),
	      (party_set_slot, ":orig_center", slot_town_prosperity, ":prosperity"),
	      (party_set_slot, ":new_center", slot_construction_type, spt_future_village),
	      (party_set_slot, ":new_center", slot_construction_time, ":time"),
	  (else_try),
	      (eq, spt_castle, ":spt"),
	      (val_mul, ":time", 1.5),
	      (val_sub, ":prosperity", 25),
	      (val_clamp, ":prosperity", 5, 80),
	      (party_set_slot, ":orig_center", slot_town_prosperity, ":prosperity"),
	      (party_set_slot, ":new_center", slot_construction_type, spt_future_castle),
	      (party_set_slot, ":new_center", slot_construction_time, ":time"),
	  (else_try),
	  	  (eq, spt_town, ":spt"),
	  	  (val_mul, ":time", 2),
	      (val_sub, ":prosperity", 30),
	      (val_clamp, ":prosperity", 5, 80),
	      (party_set_slot, ":orig_center", slot_town_prosperity, ":prosperity"),
	  	  (party_set_slot, ":new_center", slot_construction_type, spt_future_town),
	  	  (party_set_slot, ":new_center", slot_construction_time, ":time"),
	  (try_end),
	 ]),
	
	# "script_transfer_settlement"
	# Description: Transfer all information from settlement a onto settlement b, so that a can be reused
	# Input: arg1: ":source", arg2: ":target"
	# Output: none
	("transfer_settlement",
	 [ 											#Check Do we need to clear slots of source. Problem, setting all to 0, assigns some to player, like market_town, town_lord, etc.
	   (store_script_param_1, ":source"),
	   (store_script_param_2, ":target"),
	   	#collecting all info
	   (str_store_party_name, s1, ":source"),
	   (store_faction_of_party, ":faction", ":source"),
	   (party_get_position, pos1, ":source"),
	   (party_get_icon, ":icon", ":source"),
	   (party_get_slot, ":state", ":source", slot_village_state),

	   	#setting all info
	   (enable_party, ":target"),
	   (party_set_name, ":target", s1),
	   (party_set_faction, ":target", ":faction"),
	   (party_set_icon, ":target", ":icon"),
	   (party_set_position, ":target", pos1),
	   (party_set_slot, ":target", slot_village_state, ":state"),
	   (party_set_note_available, ":target", 1),
	   # slot transfer
	   (try_for_range, ":cur_slot", 0, 1000),
	      (party_get_slot, ":cur_value", ":source", ":cur_slot"),
	      (party_set_slot, ":target", ":cur_slot", ":cur_value"),
	   (try_end),
	   # party ai object transfer 
	   (try_for_parties, ":party_no"),
	   	  (party_is_active, ":party_no"),
	      (try_begin),
	          (get_party_ai_object, ":ai_object", ":party_no"),
	          (eq, ":ai_object", ":source"),
	          (party_set_ai_object, ":party_no", ":target"),
	      (try_end),
	      (try_begin), # attached parties transfer
	          (party_get_attached_to, ":cur_party", ":party_no"),
	          (eq, ":cur_party", ":source"),
	          (party_attach_to_party, ":party_no", ":target"),
	      (try_end),
	   (try_end),
        # faction ai object transfer 
       (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
          (faction_slot_eq, ":cur_kingdom", slot_faction_ai_object, ":source"),
          (faction_set_slot, ":target", slot_faction_ai_object, ":target"),
       (try_end),
       (assign, "$g_move_heroes", 1),
       (call_script, "script_party_add_party", ":target", ":source"),
       (assign, "$g_move_heroes", 0),
        # setting flags. Not sure how to clone, just set them according to type 
       (try_begin),
          (party_slot_eq, ":target_center", slot_party_type, spt_town),
          (party_set_flags, ":target_center", pf_town),
       (else_try),
          (party_slot_eq, ":target_center", slot_party_type, spt_castle),
          (party_set_flags, ":target_center", pf_castle),
       (else_try),
          (party_slot_eq, ":target_center", slot_party_type, spt_village),
          (party_set_flags, ":target_center", pf_village),                           
       (try_end),
       (party_clear_particle_systems, ":source"),
       (party_set_slot, ":source", slot_village_state, svs_normal), #sfs or svs?
       # ... inc. ... # 
	 ]),

	# "script_build_village"
	# Description: Builds the village. ":center_no" is the temporary construction site. ":orig_center" is the center, that built the settlement. ":new_center" is the settlement that gets built ingame
	# For this to make sense, only build villages from towns.
	# Input: arg1: ":center_no"
	# Output: none
	("build_village", 
	 [
	    (store_script_param_1, ":temp_center"),
	    
	    (party_get_slot, ":faction", ":temp_center", slot_construction_faction),
	    (party_get_slot, ":town_lord", ":temp_center", slot_construction_lord),
	    (party_get_position, pos1, ":temp_center"),
	    (party_get_current_terrain, ":terrain", ":temp_center"),
	    (party_get_slot, s1, ":temp_center", slot_orig_name),
        (party_get_slot, ":orig_center", ":temp_center", slot_constructing_center),
        (faction_get_slot, ":culture", ":faction", slot_faction_culture),
        (store_current_day, ":cur_day"),
        
          
        (assign, ":center_no", villages_end),
        (assign, ":original_faction", ":faction"),
        (store_sub, ":cur_prosperity", ":prosperity", 20),
        (val_clamp, ":cur_prosperity", 10, 80),
        (store_mul, ":cur_wealth", ":cur_prosperity", 10),
          
        (enable_party, ":center_no"),
        (party_set_note_available, ":center_no", 1),
        (party_set_position, ":center_no", pos1),
        (party_set_name, ":center_no", s1),
        (party_set_faction, ":center_no", ":faction"),
        (party_set_flags, ":center_no", pf_village),

        (party_set_slot, ":center_no", slot_town_lord, ":town_lord"),
        (party_set_slot, ":center_no", slot_party_type, spt_village),
        (party_set_slot, ":center_no", slot_town_prosperity, ":cur_prosperity"),
        (party_set_slot, ":center_no", slot_town_wealth, ":cur_wealth"),
        (party_set_slot, ":center_no", slot_village_market_town, ":orig_center"),    # If someone decides to build villages without a town as origin, this will fail and it would be necessary to reassign all village market towns
        (party_set_slot, ":center_no", slot_village_bound_center, ":orig_center"),
        (party_set_slot, ":center_no", slot_center_culture,  ":culture"),
        (party_set_slot, ":center_no", slot_center_original_faction,  ":original_faction"),
        (party_set_slot, ":center_no", slot_center_ex_faction,  ":original_faction"),
        (party_set_slot, ":center_no", dplmc_slot_center_ex_lord, ":town_lord"),
        (party_set_slot, ":center_no", slot_center_last_spotted_enemy, -1),
        (party_set_slot, ":center_no", slot_center_is_besieged_by, -1),
        (party_set_slot, ":center_no", slot_center_last_taken_by_troop, -1),
        (party_set_slot, ":center_no", slot_center_last_spotted_enemy, -1),
        (party_set_slot, ":center_no", slot_village_raided_by, -1),
        (party_set_slot, ":center_no", slot_day_center_built, ":cur_day"),
        (remove_party, ":temp_party"),
        (val_add, "$g_villages_end", 1),
        
        (try_for_range, ":item_no", trade_goods_begin, trade_goods_end),
        	(store_sub, ":offset", ":item_no", trade_goods_begin),
        	(val_add, ":offset", slot_town_trade_good_prices_begin),
        	(party_set_slot, ":center_no", ":offset", average_price_factor),
        (try_end),
        
          (assign, ":end_cond", village_elders_end),
          (try_for_range, ":new_elder", village_elders_begin, ":end_cond"),
              (neg|troop_slot_eq, ":new_elder", slot_trp_is_active, 1),
              (party_set_slot, ":center_no", slot_town_elder, ":new_elder"),
              (troop_set_slot, ":new_elder", slot_trp_is_active, 1),
              (assign, ":end_cond", ":new_elder"),               
          (try_end),
          (try_for_range, ":offset", dplmc_slot_town_merchants_begin, dplmc_slot_town_merchants_end),
             (party_get_slot, ":npc", ":center_no", ":offset"),
             (gt, ":npc", 0),
             (neg|troop_slot_ge, ":npc", slot_troop_home, 1),#If the startup script wasn't altered by another mod, we don't have to worry about this condition.
             (troop_set_slot, ":npc", slot_troop_home, ":center_no"),
          (try_end),
          (try_begin),
             (party_set_slot, ":center_no", dplmc_slot_center_ex_lord, ":town_lord"),
             (ge, ":town_lord", 0),
             (troop_slot_eq, ":town_lord", slot_troop_home, ":center_no"),
             (neg|party_slot_ge, ":center_no", dplmc_slot_center_original_lord, 1),
             (party_set_slot, ":center_no", dplmc_slot_center_original_lord, ":town_lord"),
          (try_end),
            (party_get_slot, ":prosperity_factor", ":center_no", slot_town_prosperity),#modify plus or minus 40% based on prosperity
            (val_clamp, ":prosperity_factor", 0, 101),
            (val_add, ":prosperity_factor", 75),#average 125, min 75, max 175          
            (store_random_in_range, ":last_arrived", 1, (24 * 7) + 1),
            (val_mul, ":last_arrived", -1),#some time in the last 7 days, plus or minus 40%
            (val_mul, ":last_arrived", 125),
            (val_div, ":last_arrived", ":prosperity_factor"),
            (party_set_slot, ":center_no", dplmc_slot_village_trade_last_returned_from_market, ":last_arrived"),
            (store_random_in_range, ":last_arrived", 1, (24 * 7) + 1),
            (val_mul, ":last_arrived", -1),#some time in the last 7 days
            (val_mul, ":last_arrived", 125),
            (val_div, ":last_arrived", ":prosperity_factor"),
            (party_set_slot, ":center_no", dplmc_slot_village_trade_last_arrived_to_market, ":last_arrived"),
            (store_random_in_range, ":troop_no", village_specialist_begin, village_specialist_end),
          (party_set_slot, ":center_no", slot_center_specialist_type, ":troop_no"),
          (store_random_in_range, ":amount", 1, 3),
          (party_set_slot, ":center_no", slot_center_specialist_amount, ":amount"), 
          
          (try_for_range, ":walker_no", 0, num_town_walkers),
               (call_script, "script_center_set_walker_to_type", ":center_no", ":walker_no", walkert_default),
          (try_end),
	      
          #Setting scenes
        (try_begin),
        	(this_or_next|eq, ":terrain", rt_snow_forest),
            (eq, ":terrain", rt_snow),
            (call_script, "script_list_random", "trp_snow_villages"),
            (assign, ":offset", reg1),
            (party_set_icon, ":center_no", "icon_village_snow_a"),
        (else_try),
            (this_or_next|eq, ":terrain", rt_desert_forest),
            (eq, ":terrain", rt_desert),
            (call_script, "script_list_random", "trp_desert_villages"),
            (assign, ":offset", reg1),
            (party_set_icon, ":center_no", "icon_village_c"),
        (else_try),
        	(call_script, "script_list_random", "trp_plain_villages"),
        	(assign, ":offset", reg1),
        	(party_set_icon, ":center_no", "icon_village_a"),
        (try_end),
          (store_add, ":exterior_scene_no", "scn_village_1", ":offset"),  
          (party_set_slot,":center_no", slot_castle_exterior, ":exterior_scene_no"),         
        

          (call_script, "script_start_refresh_village_defenders", ":center_no"),
          (call_script, "script_start_refresh_village_defenders", ":center_no"),
          (call_script, "script_start_refresh_village_defenders", ":center_no"),
          (call_script, "script_start_refresh_village_defenders", ":center_no"),
          (call_script, "script_start_give_center_to_lord", ":center_no",  ":town_lord", 0),    #F&B Check do we really run this for a village
         
	 ]),

	# "script_build_castle"
	# Description
	# Input: arg1: ":center_no"
	# Output: none
	("build_castle",			
	 [
	    (store_script_param_1, ":temp_center"),
	    
	    (party_get_slot, ":faction", ":temp_center", slot_construction_faction),
	    (party_get_slot, ":town_lord", ":temp_center", slot_construction_lord),
	    (party_get_position, pos1, ":temp_center"),
	    (party_get_current_terrain, ":terrain", ":temp_center"),
	    (party_get_slot, s1, ":temp_center", slot_orig_name),
        (party_get_slot, ":orig_center", ":temp_center", slot_constructing_center),
        (faction_get_slot, ":culture", ":faction", slot_faction_culture),
        (party_get_slot, ":prosperity", ":orig_center", slot_town_prosperity),
        (store_current_day, ":cur_day"),
        
        (remove_party, ":temp_party"),
        (call_script, "script_transfer_settlement", villages_begin, villages_end),
        (assign, ":center_no", villages_begin),

        (val_add, "$g_villages_begin", 1),
        (val_add, "$g_villages_end", 1),
        (store_sub, ":cur_prosperity", ":prosperity", 20),
        (val_clamp, ":cur_prosperity", 10, 80),
        (store_mul, ":cur_wealth", ":cur_prosperity", 20),
        

        (enable_party, ":center_no"),
        (party_set_note_available, ":center_no", 1),
        (party_set_position, ":center_no", pos1),
        (party_set_name, ":center_no", s1),
        (party_set_faction, ":center_no", ":faction"),
        (party_set_flags, ":center_no", pf_castle),

        (party_set_slot, ":center_no", slot_town_lord, ":town_lord"),
        (party_set_slot, ":center_no", slot_party_type, spt_castle),
        (party_set_slot, ":center_no", slot_town_prosperity, ":cur_prosperity"),
        (party_set_slot, ":center_no", slot_town_wealth, ":cur_wealth"),
        (party_set_slot, ":center_no", slot_center_culture,  ":culture"),
        (party_set_slot, ":center_no", slot_center_original_faction,  ":original_faction"),
        (party_set_slot, ":center_no", slot_center_ex_faction,  ":original_faction"),
        (party_set_slot, ":center_no", dplmc_slot_center_ex_lord, ":town_lord"),
        (party_set_slot, ":center_no", slot_center_last_spotted_enemy, -1),
        (party_set_slot, ":center_no", slot_center_is_besieged_by, -1),
        (party_set_slot, ":center_no", slot_center_last_taken_by_troop, -1),
        (party_set_slot, ":center_no", slot_center_last_spotted_enemy, -1),
        (party_set_slot, ":center_no", slot_village_raided_by, -1),  
        (party_set_slot, ":center_no", slot_village_state, 0),
        (party_set_slot, ":center_no", slot_town_player_odds, 1000),
        (party_set_slot, ":center_no", slot_day_center_built, ":cur_day"),

          # Setting Chest
            (assign, ":end_cond", "trp_castle_1_seneschal"),
            (try_for_range, ":cur_object_no", "trp_town_1_seneschal", ":end_cond"),
              (troop_slot_eq, ":cur_object_no", slot_trp_is_active, 0),   
              (party_set_slot, ":center_no", slot_town_seneschal, ":cur_object_no"),
              (troop_set_slot, ":cur_object_no", slot_trp_is_active, 1),
              (assign, ":end_cond", ":cur_object_no"),        #break   
            (try_end),

             ##diplomacy start+ Set the home slots for town merchants, elders, etc. for reverse-lookup
            (try_for_range, ":offset", dplmc_slot_town_merchants_begin, dplmc_slot_town_merchants_end),
              (party_get_slot, ":npc", ":center_no", ":offset"),
              (gt, ":npc", 0),
              (neg|troop_slot_ge, ":npc", slot_troop_home, 1),#If the startup script wasn't altered by another mod, we don't have to worry about this condition.
              (troop_set_slot, ":npc", slot_troop_home, ":center_no"),
            (try_end),
              ##diplomacy end+   
         (try_begin),				#this block might be unneccessary. New build settlement can never have slot_troop_home set
              (party_set_slot, ":center_no", dplmc_slot_center_ex_lord, ":town_lord"),
              (ge, ":town_lord", 0),
              (troop_slot_eq, ":town_lord", slot_troop_home, ":center_no"),
              (neg|party_slot_ge, ":center_no", dplmc_slot_center_original_lord, 1),
              (party_set_slot, ":center_no", dplmc_slot_center_original_lord, ":town_lord"),
         (try_end),

          (assign, ":garrison_strength", 15),
          (try_for_range, ":unused", 0, ":garrison_strength"),
              (call_script, "script_cf_reinforce_party", ":center_no"),
          (try_end),

          (store_random_in_range, ":troop_no", castle_specialist_begin, castle_specialist_end),
          (party_set_slot, ":center_no", slot_center_specialist_type, ":troop_no"),
          (store_random_in_range, ":amount", 1, 3),
          (party_set_slot, ":center_no", slot_center_specialist_amount, ":amount"),

          #Setting scenes
           (try_begin),
        	(this_or_next|eq, ":terrain", rt_snow_forest),
            (eq, ":terrain", rt_snow),
            (call_script, "script_list_random", "trp_snow_castles"),
            (assign, ":offset", reg1),
        (else_try),
            (this_or_next|eq, ":terrain", rt_desert_forest),
            (eq, ":terrain", rt_desert),
            (call_script, "script_list_random", "trp_desert_castles"),
            (assign, ":offset", reg1),
        (else_try),
        	(call_script, "script_list_random", "trp_plain_castles"),
        	(assign, ":offset", reg1),
        (try_end),
        (assign, ":offset_orig", ":offset"),
            (val_mul, ":offset", 3),    #F&B Check no idea, why this mul by 3 is used.
            (store_add, ":exterior_scene_no", "scn_castle_1_exterior", ":offset"),
            (party_set_slot,":center_no", slot_castle_exterior, ":exterior_scene_no"),
            (store_add, ":interior_scene_no", "scn_castle_1_interior", ":offset"),
            (party_set_slot,":center_no", slot_town_castle, ":interior_scene_no"),
            (store_add, ":interior_scene_no", "scn_castle_1_prison", ":offset"),
            (party_set_slot,":center_no", slot_town_prison, ":interior_scene_no"),
            (party_set_slot,":center_no", slot_town_reinforcement_party_template, "pt_center_reinforcements"),
            (store_random_in_range, ":rand_castle_icon", "icon_castle_derchios", "icon_castle_weyyah"),
            (party_set_icon, ":center_no", ":rand_castle_icon"), 
               # Check, whether castle needs to be sieged with belfry
            (try_begin),
                (this_or_next|eq, ":offset_orig", 0),
                (this_or_next|eq, ":offset_orig", 1),
                (this_or_next|eq, ":offset_orig", 3),
                (this_or_next|eq, ":offset_orig", 6),
                (this_or_next|eq, ":offset_orig", 7),
                (this_or_next|eq, ":offset_orig", 8),
                (this_or_next|eq, ":offset_orig", 10),
                (this_or_next|eq, ":offset_orig", 12),
                (this_or_next|eq, ":offset_orig", 20),
                (this_or_next|eq, ":offset_orig", 24),
                (this_or_next|eq, ":offset_orig", 33),
                (this_or_next|eq, ":offset_orig", 34),
                (this_or_next|eq, ":offset_orig", 37),
                (this_or_next|eq, ":offset_orig", 39),
                (this_or_next|eq, ":offset_orig", 40),
                (this_or_next|eq, ":offset_orig", 41),
                (eq, ":offset_orig", 42),
                (party_set_slot, ":center_no", slot_center_siege_with_belfry, 1),   
            (try_end),
	 ]),

	# "script_build_town"
	# Description
	# Input: arg1: ":orig_center"
	# Output: none
	("build_town",				#Need to set Scenes and Reassign village market towns?
	 [ (store_script_param_1, ":source"),
	 	
	    (party_get_slot, ":faction", ":source", slot_construction_faction),
	    (party_get_slot, ":town_lord", ":source", slot_construction_lord),
	    (party_get_position, pos1, ":source"),
	    (party_get_current_terrain, ":terrain", ":source"),
	    (party_get_slot, s1, ":source", slot_orig_name),
        (party_get_slot, ":orig_center", ":source", slot_constructing_center),
        (faction_get_slot, ":culture", ":faction", slot_faction_culture),
        (party_get_slot, ":prosperity", ":orig_center", slot_town_prosperity),
        (party_get_slot, ":wealth", ":orig_center", slot_town_wealth),
        (store_current_day, ":cur_day"),

        (val_sub, "$g_towns_begin", 1),
        (assign, ":center_no", "$g_towns_begin"),
        (store_random_in_range, ":population", 3000, 6000),
        (store_div, ":acres", ":population", 500),
       
        (enable_party, ":center_no"),
        (party_set_note_available, ":center_no", 1),
        (party_set_position, ":center_no", pos1),
        (party_set_name, ":center_no", s1),
        (party_set_faction, ":center_no", ":faction"),
        (party_set_flags, ":center_no", pf_town),

        (party_set_slot, ":center_no", slot_town_lord, ":town_lord"),
        (party_set_slot, ":center_no", slot_party_type, spt_town),
        (party_set_slot, ":center_no", slot_town_prosperity, ":prosperity"),
        (party_set_slot, ":center_no", slot_town_wealth, ":wealth"),
        (party_set_slot, ":center_no", slot_center_culture, ":culture"),
        (party_set_slot, ":center_no", slot_center_original_faction, ":original_faction"),
        (party_set_slot, ":center_no", slot_center_ex_faction, ":original_faction"),
        (party_set_slot, ":center_no", dplmc_slot_center_ex_lord, ":town_lord"),
        (party_set_slot, ":center_no", slot_center_last_spotted_enemy, -1),
        (party_set_slot, ":center_no", slot_center_is_besieged_by, -1),
        (party_set_slot, ":center_no", slot_center_last_taken_by_troop, -1),
        (party_set_slot, ":center_no", slot_center_last_spotted_enemy, -1),
        (party_set_slot, ":center_no", slot_village_raided_by, -1),  
        (party_set_slot, ":center_no", slot_village_state, 0),
        (party_set_slot, ":center_no", slot_town_player_odds, 1000),
        (party_set_slot, ":center_no", slot_center_population, ":population"),
        (party_set_slot, ":center_no", slot_town_acres, ":acres"),
        (party_set_slot, ":center_no", slot_town_reinforcement_party_template, "pt_center_reinforcements"),  
        (party_set_slot, ":center_no", slot_day_center_built, ":cur_day"),

	    (assign, ":end_cond", "trp_castle_1_seneschal"),
	    (try_for_range, ":cur_object_no", "trp_town_1_seneschal", ":end_cond"),
	      (troop_slot_eq, ":cur_object_no", slot_trp_is_active, 0),   
	      (party_set_slot, ":center_no", slot_town_seneschal, ":cur_object_no"),
	      (troop_set_slot, ":cur_object_no", slot_trp_is_active, 1),
	      (assign, ":end_cond", ":cur_object_no"),        #break   
	    (try_end),
	    (try_for_range, ":item_no", trade_goods_begin, trade_goods_end),
	        (store_sub, ":offset", ":item_no", trade_goods_begin),
	        (val_add, ":offset", slot_town_trade_good_prices_begin),
	      (party_set_slot, ":center_no", ":offset", average_price_factor),   #F&B Check should make goods initiatelly more expensive for new towns, not avg.             
	    (try_end), 
	    (assign, ":end_cond", mayors_end),
        (try_for_range, ":free_mayor", mayors_begin, ":end_cond"),
          (troop_slot_eq, ":free_mayor", slot_trp_is_active, 0),        # Since we assign all troops at the same time, if mayor 25 is unused, all other 25th troops should be unused as well. Should be always true. So realistically, setting trp_is_active for other troops is not required, however, just do it for safety. Though we never check for it, yet.
          (store_sub, ":offset", ":free_mayor", mayors_begin),
          (store_add, ":cur_object_no", "trp_town_1_mayor", ":offset"),
          (party_set_slot,":center_no", slot_town_elder, ":cur_object_no"),
          (troop_set_slot, ":cur_object_no", slot_trp_is_active, 1),
          (store_add, ":cur_object_no", "trp_town_1_tavernkeeper", ":offset"),
          (party_set_slot,":center_no", slot_town_tavernkeeper, ":cur_object_no"),
          (troop_set_slot, ":cur_object_no", slot_trp_is_active, 1),
          (store_add, ":cur_object_no", "trp_town_1_weaponsmith", ":offset"),
          (party_set_slot,":center_no", slot_town_weaponsmith, ":cur_object_no"),
          (troop_set_slot, ":cur_object_no", slot_trp_is_active, 1),
          (store_add, ":cur_object_no", "trp_town_1_armorer", ":offset"),
          (party_set_slot,":center_no", slot_town_armorer, ":cur_object_no"),
          (troop_set_slot, ":cur_object_no", slot_trp_is_active, 1),
          (store_add, ":cur_object_no", "trp_town_1_merchant", ":offset"),
          (party_set_slot,":center_no", slot_town_merchant, ":cur_object_no"),
          (troop_set_slot, ":cur_object_no", slot_trp_is_active, 1),
          (store_add, ":cur_object_no", "trp_town_1_horse_merchant", ":offset"),
          (party_set_slot,":center_no", slot_town_horse_merchant, ":cur_object_no"),
          (troop_set_slot, ":cur_object_no", slot_trp_is_active, 1),
          (store_add, ":cur_object_no", "scn_town_1_center", ":offset"),
          (party_set_slot,":center_no", slot_town_center, ":cur_object_no"),    
          (assign, ":end_cond", ":free_mayor"),   #break 
        (try_end),
        

    #Initialize walkers
        (try_for_range, ":walker_no", 0, num_town_walkers),
            (call_script, "script_center_set_walker_to_type", ":center_no", ":walker_no", walkert_default),
        (try_end),
       
        (assign, ":garrison_strength", 40),
        (try_for_range, ":unused", 0, ":garrison_strength"),
            (call_script, "script_cf_reinforce_party", ":center_no"), #F&B check. This is cheaty. We want to transfer troops from other fiefs instead.
        (try_end),
        #Fill town food stores up to half
        (call_script, "script_center_get_food_store_limit", ":center_no"),
        (assign, ":food_store_limit", reg0),
        (val_div, ":food_store_limit", 2),
        (party_set_slot, ":center_no", slot_party_food_store, ":food_store_limit"),
        (party_set_slot, ":center_no", slot_town_player_odds, 1000),
        (try_for_range, ":cur_slot", dplmc_slot_town_trade_route_last_arrivals_begin, dplmc_slot_town_trade_route_last_arrivals_end),
        (party_slot_eq, ":center_no", ":cur_slot", 0),
        (store_random_in_range, ":last_arrived", 1, (24 * 7 * 4) + 1),#some time in the last four weeks. Once we get building quest running, we can track support caravans instead of randomizing
      (val_mul, ":last_arrived", -1),     
      (party_get_slot, ":prosperity_factor", ":center_no", slot_town_prosperity),#modify plus or minus 40% based on prosperity
      (val_clamp, ":prosperity_factor", 0, 101),
      (val_add, ":prosperity_factor", 75),
      (val_mul, ":last_arrived", 125),
      (val_div, ":last_arrived", ":prosperity_factor"),#last arrival some time in the last four weeks, plus or minus 40%
      (party_set_slot, ":center_no", ":cur_slot", ":last_arrived"),

      (store_random_in_range, ":troop_no", town_specialist_begin, town_specialist_end),
     (party_set_slot, ":center_no", slot_center_specialist_type, ":troop_no"),
     (store_random_in_range, ":amount", 1, 3),
     (party_set_slot, ":center_no", slot_center_specialist_amount, ":amount"),  
        	#disable the extra village 
        (call_script, "script_transfer_settlement", villages_end, ":orig_center"),
        (call_script, "script_give_center_to_faction", villages_end, "fac_kingdom_100"),
        (disable_party, villages_end),
        (party_set_note_available, villages_end, 0),
        (party_set_slot, villages_end, slot_party_type, 0),
        (val_sub, "$g_villages_end", 1),
        	#Setting scenes
        (try_begin),
        	(this_or_next|eq, ":terrain", rt_snow_forest),
            (eq, ":terrain", rt_snow),
            (call_script, "script_list_random", "trp_snow_towns"),
            (assign, ":offset", reg1),
        (else_try),
            (this_or_next|eq, ":terrain", rt_desert_forest),
            (eq, ":terrain", rt_desert),
            (call_script, "script_list_random", "trp_desert_towns"),
            (assign, ":offset", reg1),
        (else_try),
        	(call_script, "script_list_random", "trp_plain_towns"),
        	(assign, ":offset", reg1),
        (try_end),
        (store_add, ":cur_object_no", "scn_town_1_center", ":offset"),
        (party_set_slot,":center_no", slot_town_center, ":cur_object_no"),
        (store_add, ":cur_object_no", "scn_town_1_castle", ":offset"),
        (party_set_slot,":center_no", slot_town_castle, ":cur_object_no"),
        (store_add, ":cur_object_no", "scn_town_1_prison", ":offset"),
        (party_set_slot,":center_no", slot_town_prison, ":cur_object_no"),
        (store_add, ":cur_object_no", "scn_town_1_walls", ":offset"),
        (party_set_slot,":center_no", slot_town_walls, ":cur_object_no"),
        (store_add, ":cur_object_no", "scn_town_1_tavern", ":offset"),
        (party_set_slot,":center_no", slot_town_tavern, ":cur_object_no"),
        (store_add, ":cur_object_no", "scn_town_1_store", ":offset"),
        (party_set_slot,":center_no", slot_town_store, ":cur_object_no"),
        (store_add, ":cur_object_no", "scn_town_1_arena_alternate", ":offset"),
        (party_set_slot,":cur_object_no", slot_town_arena_alternate, ":cur_object_no"),
        (store_add, ":cur_object_no", "scn_town_1_arena", ":offset"),
        (party_set_slot,":center_no", slot_town_arena, ":cur_object_no"),
        (store_add, ":cur_object_no", "scn_town_1_alley", ":offset"),
        (party_set_slot,":center_no", slot_town_alley, ":cur_object_no"),
        (party_set_slot, ":center_no", slot_town_alternate_arena_no, ":offset"),

        (call_script, "script_initialize_town_arena_info_dynamic", ":center_no", ":offset"),
        (call_script, "script_give_center_to_faction_aux", ":center_no", ":faction"),
        (call_script, "script_start_give_center_to_lord", ":center_no", ":town_lord", 0),
        (call_script, "script_update_village_market_towns"),      #F&B check. Do we really want to run this?
        (call_script, "script_initialize_economic_information"),
        (call_script, "script_dw_establish_trade_routes"),
        
	 ]),
	# "script_downgrade_town"
	# Description
	# Input: arg1: ":center_no"
	# Output: none
	("downgrade_town", 			#Check visiting merchants and remove them, or does game do it automatically?
	 [
	    (store_script_param_1, ":source"),
	    
	    (party_get_slot, ":faction", ":source", slot_construction_faction),
	    (party_get_slot, ":town_lord", ":source", slot_construction_lord),
	    (party_get_position, pos1, ":source"),
	    (party_get_current_terrain, ":terrain", ":source"),
	    (str_store_party_name, s1, "source"),
        (faction_get_slot, ":culture", ":faction", slot_faction_culture),
        (party_get_slot, ":prosperity", ":source", slot_town_prosperity),
        (party_get_slot, ":population", ":source", slot_center_population),
        (party_get_slot, ":wealth", ":source", slot_town_wealth),
        (party_get_slot, ":original_faction", slot_center_original_faction),
        (party_get_slot, ":ex_faction", ":source", slot_center_ex_faction),
        (party_get_slot, ":ex_lord", ":source", dplmc_slot_center_ex_lord),
        (store_current_day, ":cur_day"),

        (assign, ":center_no", villages_end),
        (val_add, "$g_villages_end", 1),
        (store_sub, ":cur_prosperity", ":prosperity", 20),
        (store_sub, ":cur_wealth", ":wealth", 1000),
        (val_clamp, ":wealth", 0, 5000),

        (enable_party, ":center_no"),
        (party_set_note_available, ":center_no", 1),
        (party_set_position, ":center_no", pos1),
        (party_set_name, ":center_no", s1),
        (party_set_faction, ":center_no", ":faction"),
        (party_set_flags, ":center_no", pf_village),

        (party_set_slot, ":center_no", slot_town_lord, ":town_lord"),
        (party_set_slot, ":center_no", slot_party_type, spt_village),
        (party_set_slot, ":center_no", slot_town_prosperity, ":cur_prosperity"),
        (party_set_slot, ":center_no", slot_town_wealth, ":cur_wealth"),
        #(party_set_slot, ":center_no", slot_village_market_town, ":orig_center"),    # If someone decides to build villages without a town as origin, this will fail and it would be necessary to reassign all village market towns
        #(party_set_slot, ":center_no", slot_village_bound_center, ":orig_center"),
        (party_set_slot, ":center_no", slot_center_culture,  ":culture"),
        (party_set_slot, ":center_no", slot_center_original_faction,  ":original_faction"),
        (party_set_slot, ":center_no", slot_center_ex_faction,  ":ex_faction"),
        (party_set_slot, ":center_no", dplmc_slot_center_ex_lord, ":ex_lord"),
        (party_set_slot, ":center_no", slot_center_last_spotted_enemy, -1),
        (party_set_slot, ":center_no", slot_center_is_besieged_by, -1),
        (party_set_slot, ":center_no", slot_center_last_taken_by_troop, -1),
        (party_set_slot, ":center_no", slot_center_last_spotted_enemy, -1),
        (party_set_slot, ":center_no", slot_village_raided_by, -1),
        (party_set_slot, ":center_no", slot_former_town, 1),
        (party_set_slot, ":center_no", slot_day_center_built, ":cur_day"),

       (try_for_range, ":item_no", trade_goods_begin, trade_goods_end),
        	(store_sub, ":offset", ":item_no", trade_goods_begin),
        	(val_add, ":offset", slot_town_trade_good_prices_begin),
        	(party_set_slot, ":center_no", ":offset", average_price_factor),
        (try_end),
        
          (assign, ":end_cond", village_elders_end),
          (try_for_range, ":new_elder", village_elders_begin, ":end_cond"),
              (neg|troop_slot_eq, ":new_elder", slot_trp_is_active, 1),
              (party_set_slot, ":center_no", slot_town_elder, ":new_elder"),
              (troop_set_slot, ":new_elder", slot_trp_is_active, 1),
              (assign, ":end_cond", ":new_elder"),               
          (try_end),
          (try_for_range, ":offset", dplmc_slot_town_merchants_begin, dplmc_slot_town_merchants_end),
             (party_get_slot, ":npc", ":center_no", ":offset"),
             (gt, ":npc", 0),
             (neg|troop_slot_ge, ":npc", slot_troop_home, 1),#If the startup script wasn't altered by another mod, we don't have to worry about this condition.
             (troop_set_slot, ":npc", slot_troop_home, ":center_no"),
          (try_end),
            (party_get_slot, ":prosperity_factor", ":center_no", slot_town_prosperity),#modify plus or minus 40% based on prosperity
            (val_clamp, ":prosperity_factor", 0, 101),
            (val_add, ":prosperity_factor", 75),#average 125, min 75, max 175          
            (store_random_in_range, ":last_arrived", 1, (24 * 7) + 1),
            (val_mul, ":last_arrived", -1),#some time in the last 7 days, plus or minus 40%
            (val_mul, ":last_arrived", 125),
            (val_div, ":last_arrived", ":prosperity_factor"),
            (party_set_slot, ":center_no", dplmc_slot_village_trade_last_returned_from_market, ":last_arrived"),
            (store_random_in_range, ":last_arrived", 1, (24 * 7) + 1),
            (val_mul, ":last_arrived", -1),#some time in the last 7 days
            (val_mul, ":last_arrived", 125),
            (val_div, ":last_arrived", ":prosperity_factor"),
            (party_set_slot, ":center_no", dplmc_slot_village_trade_last_arrived_to_market, ":last_arrived"),
            (store_random_in_range, ":troop_no", village_specialist_begin, village_specialist_end),
          (party_set_slot, ":center_no", slot_center_specialist_type, ":troop_no"),
          (store_random_in_range, ":amount", 1, 3),
          (party_set_slot, ":center_no", slot_center_specialist_amount, ":amount"), 
          
          (try_for_range, ":walker_no", 0, num_town_walkers),
               (call_script, "script_center_set_walker_to_type", ":center_no", ":walker_no", walkert_default),
          (try_end),
	      
          #Setting scenes
        (try_begin),
        	(this_or_next|eq, ":terrain", rt_snow_forest),
            (eq, ":terrain", rt_snow),
            (call_script, "script_list_random", "trp_snow_villages"),
            (assign, ":offset", reg1),
            (party_set_icon, ":center_no", "icon_village_snow_a"),
        (else_try),
            (this_or_next|eq, ":terrain", rt_desert_forest),
            (eq, ":terrain", rt_desert),
            (call_script, "script_list_random", "trp_desert_villages"),
            (assign, ":offset", reg1),
            (party_set_icon, ":center_no", "icon_village_c"),
        (else_try),
        	(call_script, "script_list_random", "trp_plain_villages"),
        	(assign, ":offset", reg1),
        	(party_set_icon, ":center_no", "icon_village_a"),
        (try_end),
          (store_add, ":exterior_scene_no", "scn_village_1", ":offset"),  
          (party_set_slot,":center_no", slot_castle_exterior, ":exterior_scene_no"),         
        

          
        ###### Exodus begin ######
       	# Some deserters.
       	(store_div, ":deserter_no", ":population", 100),

       	(set_spawn_radius, 2),

       	(store_random_in_range, ":rand", 1, 4),
       	(assign, ":end_cond", ":rand"),
       	(try_for_range, ":loop_no", 1, ":end_cond"),
       		(spawn_around_party, ":source", "pt_deserters"),
       		(party_set_name, reg0, "@ Deserters from {s1}"),
       		(assign, ":party_no", reg0),
       		(store_random_in_range, ":rand", 3, 10),
       		(val_mul, ":deserter_no", ":rand"),
       		(party_add_members, ":party_no", "trp_woman_r_peasant", ":deserter_no"),
       	(try_end),
       	# other inhabitants flee to nearby centers

       	(val_sub, ":population", ":deserter_no"),
       	(val_div, ":population", 3),
       	(assign, ":max_dist", 50),
       	(assign, ":total_deserters", 0),
       	(set_spawn_radius, 0),
       	(assign, ":end_cond", centers_end),
       	(try_for_range, ":cur_center", centers_begin, ":end_cond"),
       		(neq, ":cur_center", ":center_no"),
       		(neq, ":cur_center", ":source"),
       		#(neq|party_slot_eq, ":cur_center", slot_receiving_refugees, 1), #exclude centers already receiving refugees from this town
       		(store_distance_to_party_from_party, ":cur_dist", ":source", ":cur_center"),
       		(le, ":cur_dist", ":max_dist"),
       		(try_begin),
       		    (party_slot_eq, ":cur_center", slot_party_type, spt_town),
       		    (store_random_in_range, ":deserter_no", 100, 200),
       		(else_try),
       		    (party_slot_eq, ":cur_center", slot_party_type, spt_castle),
       		    (store_random_in_range, ":deserter_no", 30, 50),
       		(else_try),
       		    (party_slot_eq, ":cur_center", slot_party_type, spt_village),
       		    (store_random_in_range, ":deserter_no", 20, 150),
       		(try_end),

       		(spawn_around_party, ":source", "pt_town_runaways"),
       		(party_add_members, reg0, "trp_mercenary_e_townsman", ":deserter_no"),
       		#(party_set_slot, ":cur_center", slot_receiving_refugees, 1),
       		(val_add, ":total_deserters", ":deserter_no"),
       		(try_begin),
       			(ge, ":total_deserters", ":population"),
       			(assign, ":end_cond", ":cur_center"),	#break
       		(try_begin),
       	(try_end),
       	(try_begin),
       		(gt, ":population", ":total_deserters"),	#still people left over can support construction sites
       		(try_for_parties, ":party_no"),
       			(gt, ":population", ":total_deserters"),		#yes, we check again for each party.
       			(party_is_active, ":party_no"),
       			(party_slot_eq, ":party_no", slot_in_construction, 1),
       			(store_random_in_range, ":rand1", 20, 50),
       			(store_random_in_range, ":rand2", 15, 40),
       			(spawn_around_party, ":source", "pt_town_runaways"),
       			(assign, ":cur_party", reg0),
       			(party_add_members, ":cur_party", "trp_mercenary_e_townsman", ":rand1"),
       			(party_add_members, ":cur_party", "trp_woman_e_peasant", ":rand2"),
       			(val_add, ":total_deserters", ":rand1"),
       			(val_add, ":total_deserters", ":rand2"),
       		(try_end),
       	(try_end),
       	###### Exodus end ######
       	(try_for_parties, ":party_no"),		#nearby bound villages need to get unbound.
       		(party_is_active, ":party_no"),
       		(party_slot_eq, ":party_no", slot_village_market_town, ":source"),
       		(party_set_slot, ":party_no", slot_village_market_town, -1),
       		(party_set_slot, ":party_no", slot_village_bound_center, -1),
       	(try_end),

       	# disable first town  and if necessary, transfer first town onto downgraded town, before disabling the first town.
       	(try_begin),
       		(neq, ":source", towns_begin),
       		(call_script, "script_transfer_settlement", towns_begin, ":source"),
       	(try_end),

       	(assign, ":party_to_remove", towns_begin),
       	(party_clear, ":party_to_remove"),
       	(disable_party, ":party_to_remove"),
		(party_set_note_available, ":party_to_remove", 0),
		(call_script, "script_give_center_to_faction_aux", ":party_to_remove", "fac_kingdom_100"),  
		(party_set_slot, ":party_to_remove", slot_party_type, 0),
		(val_add, "$g_towns_begin", 1),

        (call_script, "script_start_refresh_village_defenders", ":center_no"),
        (call_script, "script_start_refresh_village_defenders", ":center_no"),
        (call_script, "script_start_refresh_village_defenders", ":center_no"),
        (call_script, "script_start_refresh_village_defenders", ":center_no"),
        (call_script, "script_start_give_center_to_lord", ":center_no",  ":town_lord", 0),    #F&B Check do we really run this for a village
         
       	(call_script, "script_update_village_market_towns"),

	 ]),

	# "script_destroy_village"
	# Description: Remove a village from the game completely
	# Input: arg1: ":center_no"
	# Output: none
	("destroy_village",
	 [
	    (store_script_param_1, ":center_no"),
        
        (str_store_party_name, s1, ":center_no"),
        (store_faction_of_party, ":faction", ":center_no"),
        (party_get_slot, ":town_lord", ":center_no", slot_town_lord),
        (str_store_troop_name, s2, ":town_lord"),
        
        (store_sub, ":last_village", villages_end, 1),
	    (try_begin),
            (neq, ":center_no", ":last_village"),
            (call_script, "script_transfer_settlement", ":last_village", ":center_no"),
        (try_begin),

        (val_sub, "$g_villages_end", 1),
        (party_clear, ":last_village"),
        (disable_party, ":last_village"),
        (party_set_note_available, ":last_village", 0),
        (call_script, "script_give_center_to_faction_aux", ":last_village", "fac_kingdom_100"),
        (party_set_slot, ":last_village", slot_party_type, 0),
        (party_set_slot, ":last_village", slot_village_bound_center, -1),
        (party_set_slot, ":last_villlage", slot_village_market_town, -1),
        
        (display_message, "@ The fighting around {s1) has taken it's toll on the settlement. It has been utterly destroyed. You hear that {s2} is furious about the loss!"),
        
	    
	 ]),
   #End
   ]