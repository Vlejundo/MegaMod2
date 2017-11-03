from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *
from header_music import *
##diplomacy start+
from header_terrain_types import *
from module_constants import *
from module_factions import dplmc_factions_end
##diplomacy end+
from dsettlements_constants import *
from dsettlements_quests import *

####################################################################################################################
# Simple triggers are the alternative to old style triggers. They do not preserve state, and thus simpler to maintain.
#
#  Each simple trigger contains the following fields:
# 1) Check interval: How frequently this trigger will be checked
# 2) Operation block: This must be a valid operation block. See header_operations.py for reference.
####################################################################################################################



simple_triggers = [
	#F&B Checks for finished constructions and replaces with the actual settlements
	(24*7, 
		[
		(try_for_parties, ":party_no"),
			(party_is_active, ":party_no"),
			(party_slot_eq, ":party_no", slot_in_construction, 1),
			
			(party_get_slot, ":start_day", ":party_no", slot_construction_started),
			(party_get_slot, ":build_time", ":party_no", slot_construction_time),
			(store_time_of_day, ":cur_day"),
			
			(store_sub, ":days_passed", ":cur_day", ":start_day"),
			
			(ge, ":days_passed", ":build_time"),
  
            (try_begin),
                (party_slot_eq, ":party_no", slot_construction_type, spt_future_village),
                (call_script, "script_build_village", ":party_no"),
            (else_try),
                (party_slot_eq, ":party_no", slot_construction_type, spt_future_castle),
                (call_script, "script_build_castle", ":party_no"),
            (else_try),
                (party_slot_eq, ":party_no", slot_construction_type, spt_future_town),
                (call_script, "script_build_town", ":party_no"),
            (try_end),

		(try_end),

		]),	

	# Trigger, which activates settlement upgrade quest 
	(24*14, 
		[
		(try_for_range, ":cur_center", centers_begin, centers_end),
			(party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
			(neq|check_quest_active, "qst_construct_settlement"),
			(party_get_slot, ":prosperity", ":cur_center", slot_town_prosperity),
			(party_get_slot, ":last_transfer", ":cur_center", dplmc_slot_center_last_transfer_time),
			(party_get_slot, ":day_built", ":cur_center", slot_day_center_built),
			(party_get_slot, ":population", ":cur_center", slot_center_population),
			(party_get_slot, ":village_elder", ":cur_center", slot_town_elder), 
			(store_current_day, ":cur_day"),

			(store_sub, ":days_since_built", ":cur_day", ":day_built"),
			(store_sub, ":days_since_transfer", ":cur_day", ":last_transfer"),

			(assign, ":construct", 0),
			(try_begin),
			    (party_slot_eq, ":cur_center", slot_party_type, spt_town),
			    (ge, ":prosperity", 90),
			    (ge, ":days_since_built", 180), 	# >half a year since settlement constructed
			    							# or it was already constructed before game started
				(ge, ":days_since_transfer", 60),	# >2 month of current lord
				(ge, ":population", 30000),
				(assign, ":construct", 1),	
			(else_try),
			    (party_slot_eq, ":cur_center", slot_party_type, spt_village),
			    (ge, ":prosperity", 85),
			    (ge, ":days_since_built", 90),		# >3 month since settlement constructed
			    (ge, ":days_since_transfer", 60),	# >2 month of current lord
			    (assign, ":construct", 1), 
			(try_end),

			(eq, ":construct", 1),	# go ahead 

			(call_script, "script_start_quest", "qst_construct_settlement", ":village_elder"),
			(quest_set_slot, "qst_construct_settlement", slot_quest_constructing_center, ":cur_center"),
			(quest_set_slot, "qst_construct_settlement", slot_quest_dont_give_again_period, 60), 
		(try_end),
### slot_quest_dont_give_again_period

		]),
	#End
	]