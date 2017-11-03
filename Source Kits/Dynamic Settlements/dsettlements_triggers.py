from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *

#from module_troops import * #for 
from dsettlements_constants import *
from module_constants import *
#from dsettlements_troops import *

####################################################################################################################
#  Each trigger contains the following fields:
# 1) Check interval: How frequently this trigger will be checked
# 2) Delay interval: Time to wait before applying the consequences of the trigger
#    After its conditions have been evaluated as true.
# 3) Re-arm interval. How much time must pass after applying the consequences of the trigger for the trigger to become active again.
#    You can put the constant ti_once here to make sure that the trigger never becomes active again after it fires once.
# 4) Conditions block (list). This must be a valid operation block. See header_operations.py for reference.
#    Every time the trigger is checked, the conditions block will be executed.
#    If the conditions block returns true, the consequences block will be executed.
#    If the conditions block is empty, it is assumed that it always evaluates to true.
# 5) Consequences block (list). This must be a valid operation block. See header_operations.py for reference. 
####################################################################################################################

# Some constants for use below
triggers = [

#F&B begin 
################## Filling the lists with names Hella awkward, but we only need to do this once
####### Would be much easier to sort the settlements by faction, as that would enable try_for_range list filling
(0.0, 0, ti_once,[],  # Idea: Could further divide into wooden and stone settlements
[
(call_script, "script_list_clear", "trp_plain_name"),
(try_for_range, ":name", "str_name_200", "str_name_300"),
  (call_script, "script_list_add", "trp_plain_name", ":name"),
(try_end),
(call_script, "script_list_clear", "trp_coastal_name"),
(try_for_range, ":name", "str_name_1", "str_name_32"),
  (call_script, "script_list_add", "trp_coastal_name", ":name"),
(try_end),
(call_script, "script_list_clear", "trp_snow_name"),
(try_for_range, ":name", "str_name_50", "str_name_58"),
  (call_script, "script_list_add", "trp_snow_name", ":name"),
(try_end),
(call_script, "script_list_clear", "trp_desert_name"),
(try_for_range, ":name", "str_name_80", "str_name_84"),
  (call_script, "script_list_add", "trp_desert_name", ":name"),
(try_end),
(call_script, "script_list_clear", "trp_forest_name"),
(try_for_range, ":name", "str_name_100", "str_name_119"),
  (call_script, "script_list_add", "trp_forest_name", ":name"),
(try_end),
(call_script, "script_list_clear", "trp_mountain_name"),
(try_for_range, ":name", "str_name_150", "str_name_170"),
  (call_script, "script_list_add", "trp_mountain_name", ":name"),
(try_end),
##### Scene stuff
(call_script, "script_list_clear", "trp_desert_towns"),
(call_script, "script_list_clear", "trp_desert_castles"),
(call_script, "script_list_clear", "trp_desert_villages"),
(call_script, "script_list_clear", "trp_snow_towns"),
(call_script, "script_list_clear", "trp_snow_castles"),
(call_script, "script_list_clear", "trp_snow_villages"),
(call_script, "script_list_clear", "trp_plain_towns"),
(call_script, "script_list_clear", "trp_plain_castles"),
(call_script, "script_list_clear", "trp_plain_villages"),
  # desert towns Note. We store offset. E.g. town_19 is a desert town, it is offset by 18 from town_1
(call_script, "script_list_add", "trp_desert_towns", 18),
(call_script, "script_list_add", "trp_desert_towns", 19),
(call_script, "script_list_add", "trp_desert_towns", 20),
(call_script, "script_list_add", "trp_desert_towns", 21),
 # desert castles
(call_script, "script_list_add", "trp_desert_castles", 40),
(call_script, "script_list_add", "trp_desert_castles", 41),
(call_script, "script_list_add", "trp_desert_castles", 42),
(call_script, "script_list_add", "trp_desert_castles", 43),
(call_script, "script_list_add", "trp_desert_castles", 44),
(call_script, "script_list_add", "trp_desert_castles", 45),
(call_script, "script_list_add", "trp_desert_castles", 46),
(call_script, "script_list_add", "trp_desert_castles", 47),
 # desert villages
(try_for_range, ":party_no", "p_village_91", "p_fief_101"),     #F&B check. thing we are off by one, or off by one on all other settings
  (store_sub, ":offset", ":party_no", villages_begin),
  (call_script, "script_list_add", "trp_desert_villages", ":offset"),
(try_end),
 # snow towns
(call_script, "script_list_add", "trp_snow_towns", 8),
(call_script, "script_list_add", "trp_snow_towns", 10),
 # snow castles
(call_script, "script_list_add", "trp_snow_castles", 7),
(call_script, "script_list_add", "trp_snow_castles", 17),
(call_script, "script_list_add", "trp_snow_castles", 18),
(call_script, "script_list_add", "trp_snow_castles", 28),
(call_script, "script_list_add", "trp_snow_castles", 38),
 # snow villages
(call_script, "script_list_add", "trp_snow_villages", 13),
(call_script, "script_list_add", "trp_snow_villages", 15),
(call_script, "script_list_add", "trp_snow_villages", 16),
(call_script, "script_list_add", "trp_snow_villages", 17),
(call_script, "script_list_add", "trp_snow_villages", 18),
(call_script, "script_list_add", "trp_snow_villages", 19),
(call_script, "script_list_add", "trp_snow_villages", 20),
(call_script, "script_list_add", "trp_snow_villages", 21),
(call_script, "script_list_add", "trp_snow_villages", 48),
(call_script, "script_list_add", "trp_snow_villages", 49),
(call_script, "script_list_add", "trp_snow_villages", 61),
(call_script, "script_list_add", "trp_snow_villages", 74),
(call_script, "script_list_add", "trp_snow_villages", 84),
(call_script, "script_list_add", "trp_snow_villages", 85),

# plain settlements (neither snow, nor desert)
(try_for_range, ":party_no", "p_town_1", "p_town_19"),     #F&B check. thing we are off by one, or off by one on all other settings
  (neq, ":party_no", "p_town_9"),
  (neq, ":party_no", "p_town_11"),
  (store_sub, ":offset", ":party_no", towns_begin),
  (call_script, "script_list_add", "trp_plain_towns", ":offset"),
(try_end),
(try_for_range, ":party_no", "p_castle_1", "p_castle_41"),     #F&B check. thing we are off by one, or off by one on all other settings
  (neq, ":party_no", "p_castle_8"),
  (neq, ":party_no", "p_castle_18"),
  (neq, ":party_no", "p_castle_19"),
  (neq, ":party_no", "p_castle_29"),
  (neq, ":party_no", "p_castle_39"),
  (store_sub, ":offset", ":party_no", castles_begin),
  (call_script, "script_list_add", "trp_plain_castles", ":offset"),
(try_end),
(try_for_range, ":party_no", "p_village_1", "p_village_91"),     #F&B check. thing we are off by one, or off by one on all other settings
  (neq, ":party_no", "p_village_14"),
  (neq, ":party_no", "p_village_16"),
  (neq, ":party_no", "p_village_17"),
  (neq, ":party_no", "p_village_18"),
  (neq, ":party_no", "p_village_19"),
  (neq, ":party_no", "p_village_20"),
  (neq, ":party_no", "p_village_21"),
  (neq, ":party_no", "p_village_22"),
  (neq, ":party_no", "p_village_49"),
  (neq, ":party_no", "p_village_50"),
  (neq, ":party_no", "p_village_62"),
  (neq, ":party_no", "p_village_75"),
  (neq, ":party_no", "p_village_85"),
  (neq, ":party_no", "p_village_86"),
  (store_sub, ":offset", ":party_no", villages_begin),
  (call_script, "script_list_add", "trp_plain_villages", ":offset"),
(try_end),

## Map icon lists
(call_script, "script_list_clear", "trp_desert_town_icons"),
(call_script, "script_list_clear", "trp_desert_castle_icons"),
(call_script, "script_list_clear", "trp_snow_town_icons"),
(call_script, "script_list_clear", "trp_snow_castle_icons"),
(call_script, "script_list_clear", "trp_plain_town_icons"),
(call_script, "script_list_clear", "trp_plain_castle_icons"),
  # plain castle icons  
(try_for_range, ":cur_icon_no", "icon_castle_derchios", "icon_castle_bardaq"),
  (neq, ":cur_icon_no", "icon_castle_ismirala"),
  (neq, ":cur_icon_no", "icon_castle_jeirbe"),
  (neq, ":cur_icon_no", "icon_castle_nelag"),
  (neq, ":cur_icon_no", "icon_castle_slezkh"),
  (neq, ":cur_icon_no", "icon_castle_yruma"),
  (call_script, "script_list_add", "trp_plain_castle_icons", ":cur_icon_no"),
(try_end),
 # plain town icons
(try_for_range, ":cur_icon_no", "icon_town_mercenary_zendar", "icon_town_sarranid_ahmerrad"),
  (neq, ":cur_icon_no", "icon_town_vaegir_curaw"),
  (neq, ":cur_icon_no", "icon_town_vaegir_khudan"),
  (call_script, "script_list_add", "trp_plain_town_icons", ":cur_icon_no"),
(try_end),
 # desert castle icons
 (try_for_range, ":cur_icon_no", "icon_castle_bardaq", "icon_bridge_a"),
  (call_script, "script_list_add", "trp_desert_castle_icons", ":cur_icon_no"),
(try_end),
 # desert town icons
 (try_for_range, ":cur_icon_no", "icon_town_sarranid_ahmerrad", "icon_village_a"),
  (call_script, "script_list_add", "trp_desert_town_icons", ":cur_icon_no"),
(try_end),
 # snow castle icons
  (call_script, "script_list_add", "trp_snow_castle_icons", "icon_castle_ismirala"),
  (call_script, "script_list_add", "trp_snow_castle_icons", "icon_castle_jeirbe"),
  (call_script, "script_list_add", "trp_snow_castle_icons", "icon_castle_nelag"),
  (call_script, "script_list_add", "trp_snow_castle_icons", "icon_castle_slezkh"),
  (call_script, "script_list_add", "trp_snow_castle_icons", "icon_castle_yruma"),
 # snow town icons
  (call_script, "script_list_add", "trp_snow_town_icons", "icon_town_vaegir_curaw"),
  (call_script, "script_list_add", "trp_snow_town_icons", "icon_town_vaegir_khudan"),

  ]),
# The end
]