from header_common import *
from header_presentations import *
from header_mission_templates import *
from ID_meshes import *
from header_operations import *
from header_triggers import *
from module_constants import *
import string
from dsettlements_strings import *
## CC
from header_skills import *
from header_items import *
##diplomacy start+ Import for use with terrain advantage
from header_terrain_types import *
##diplomacy end+
from module_items import *
from module_my_mod_set import *
## CC

####################################################################################################################
#  Each presentation record contains the following fields:
#  1) Presentation id: used for referencing presentations in other files. The prefix prsnt_ is automatically added before each presentation id.
#  2) Presentation flags. See header_presentations.py for a list of available flags
#  3) Presentation background mesh: See module_meshes.py for a list of available background meshes
#  4) Triggers: Simple triggers that are associated with the presentation
####################################################################################################################

presentations = [
	       #F&B begin Rename fief 
  ("name_fief",0,mesh_load_window,[
      (ti_on_presentation_load,
       [(set_fixed_point_multiplier, 1000),
        (str_store_string, s1, "str_name_fief_text"),
        (create_text_overlay, reg1, s1, tf_center_justify),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, 500),
        (overlay_set_position, reg1, pos1),
        (overlay_set_text, reg1, s1),
        (create_simple_text_box_overlay, "$g_presentation_obj_name_fief_1"),
        (position_set_x, pos1, 400),
        (position_set_y, pos1, 400),
        (overlay_set_position, "$g_presentation_obj_name_fief_1", pos1),

        (str_store_party_name, s7, "$g_encountered_party"),
        (overlay_set_text, "$g_presentation_obj_name_fief_1", s7),

        
        (create_button_overlay, "$g_presentation_obj_name_fief_2", "@Continue...", tf_center_justify),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, 300),
        (overlay_set_position, "$g_presentation_obj_name_fief_2", pos1),
        (presentation_set_duration, 999999),
        ]),
        (ti_on_presentation_event_state_change,
       [(store_trigger_param_1, ":object"),
        (try_begin),
          (eq, ":object", "$g_presentation_obj_name_fief_1"),
          (str_store_string, s7, s0),
        (else_try),
          (eq, ":object", "$g_presentation_obj_name_fief_2"),
          #(faction_set_name, "fac_player_supporters_faction", s7),     #F&B bug fix. disabled due to renaming fief and kingdom
          (party_set_name, "$g_encountered_party", s7),
#          (faction_set_color, "fac_player_supporters_faction", 0xFF0000),
#          (assign, "$players_kingdom_name_set", 1),
          (presentation_set_duration, 0),
        (try_end),
        (change_screen_map),
        ]),
      ]),   
      ("name_new_fief",0,mesh_load_window,[
      (ti_on_presentation_load,
       [          
        (try_begin),
           (party_slot_eq, "$g_current_center", slot_party_type, spt_town),
           (str_store_string, s55, "@town"),
        (else_try),
            (party_slot_eq, "$g_current_center", slot_party_type, spt_castle),
            (str_store_string, s55, "@castle"),
        (else_try),
            (party_slot_eq, "$g_current_center", slot_party_type, spt_village),
            (str_store_string, s55, "@village"),                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
        (try_end),
        (set_fixed_point_multiplier, 1000),
        (str_store_string, s1, "str_name_fief_text_new"),
        (create_text_overlay, reg1, s1, tf_center_justify),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, 500),
        (overlay_set_position, reg1, pos1),
        (overlay_set_text, reg1, s1),
        (create_simple_text_box_overlay, "$g_presentation_obj_name_fief_1"),
        (position_set_x, pos1, 400),
        (position_set_y, pos1, 400),
        (overlay_set_position, "$g_presentation_obj_name_fief_1", pos1),

        (str_store_party_name, s7, "$g_current_center"),
        (overlay_set_text, "$g_presentation_obj_name_fief_1", s7),

        
        (create_button_overlay, "$g_presentation_obj_name_fief_2", "@Continue...", tf_center_justify),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, 300),
        (overlay_set_position, "$g_presentation_obj_name_fief_2", pos1),
        (presentation_set_duration, 999999),
        ]),
      (ti_on_presentation_event_state_change,
       [(store_trigger_param_1, ":object"),
        (try_begin),
          (eq, ":object", "$g_presentation_obj_name_fief_1"),
          (str_store_string, s7, s0),
        (else_try),
          (eq, ":object", "$g_presentation_obj_name_fief_2"),
          #(faction_set_name, "fac_player_supporters_faction", s7),
          (party_set_name, "$g_current_center", s7),
#          (faction_set_color, "fac_player_supporters_faction", 0xFF0000),
#          (assign, "$players_kingdom_name_set", 1),
          (presentation_set_duration, 0),
        (try_end),
        (change_screen_map),    #F&B bug hunting. Didn't do anything
        ]),
      ]),       
        #F&B end Rename fief

        #End 

    ]