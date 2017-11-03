# -*- coding: cp1254 -*-
from header_common import *
from header_dialogs import *
from header_operations import *
from header_parties import *
from header_item_modifiers import *
from header_skills import *
from header_triggers import *
from ID_troops import *
from ID_party_templates import *
##diplomacy start+
from header_troops import ca_intelligence
from header_terrain_types import *
from header_items import * #For ek_food, and so forth
##diplomacy end+
from module_constants import *
## CC
from header_items import *
from header_troops import *
## CC


####################################################################################################################
# During a dialog, the dialog lines are scanned from top to bottom.
# If the dialog-line is spoken by the player, all the matching lines are displayed for the player to pick from.
# If the dialog-line is spoken by another, the first (top-most) matching line is selected.
#
#  Each dialog line contains the following fields:
# 1) Dialogue partner: This should match the person player is talking to.
#    Usually this is a troop-id.
#    You can also use a party-template-id by appending '|party_tpl' to this field.
#    Use the constant 'anyone' if you'd like the line to match anybody.
#    Appending '|plyr' to this field means that the actual line is spoken by the player
#    Appending '|other(troop_id)' means that this line is spoken by a third person on the scene.
#       (You must make sure that this third person is present on the scene)
#
# 2) Starting dialog-state:
#    During a dialog there's always an active Dialog-state.
#    A dialog-line's starting dialog state must be the same as the active dialog state, for the line to be a possible candidate.
#    If the dialog is started by meeting a party on the map, initially, the active dialog state is "start"
#    If the dialog is started by speaking to an NPC in a town, initially, the active dialog state is "start"
#    If the dialog is started by helping a party defeat another party, initially, the active dialog state is "party_relieved"
#    If the dialog is started by liberating a prisoner, initially, the active dialog state is "prisoner_liberated"
#    If the dialog is started by defeating a party led by a hero, initially, the active dialog state is "enemy_defeated"
#    If the dialog is started by a trigger, initially, the active dialog state is "event_triggered"
# 3) Conditions block (list): This must be a valid operation block. See header_operations.py for reference.
# 4) Dialog Text (string):
# 5) Ending dialog-state:
#    If a dialog line is picked, the active dialog-state will become the picked line's ending dialog-state.
# 6) Consequences block (list): This must be a valid operation block. See header_operations.py for reference.
# 7) Voice-over (string): sound filename for the voice over. Leave here empty for no voice over
####################################################################################################################

dialogs = [
# Town quest
[anyone|plyr,"village_elder_talk", 
[
(check_quest_active, "qst_construct_settlement"),
(neq|check_quest_concluded, "qst_construct_settlement"),
(party_get_slot, ":village_elder", "$current_town", slot_town_elder),
(quest_slot_eq, "qst_construct_settlement", slot_quest_giver_troop, ":village_elder"),
(str_clear, s1),
(str_clear, s2),
(str_store_party_name, s1, "$g_encountered_party"),
#(str_store_faction_name, s2, ":faction"),

],
"Elder, my time is precious. What is so urgent?",
"village_elder_settlement",
[]],

[anyone, "village_elder_settlement", 
[], "Ah yes, I am glad you have arrived. People are getting anxious.",
"village_elder_settlement_2",
[]],
[anyone|plyr, "village_elder_settlement_2", 
[], "Why is that. Last time I checked, things were going fine.",
"village_elder_settlement_3",
[]],
[anyone, "village_elder_settlement_3", 
[], "Indeed, that is the case. Maybe too well. There have been increasing complaints.^There are too many people to house and fed.^Some even started to talk about leaving.",
"village_elder_settlement_4",
[]],
[anyone|plyr, "village_elder_settlement_4", 
[], "What is this nonsense!",
"village_elder_settlement_5",
[]],
[anyone, "village_elder_settlement_5", 
[], "My {lord/lady}, it is an adventerous task, but with your help, there might be enough volunteers to start construction of a new settlement.^You should decide on this matter. You could go for the military option and start construction of a new castle, or for the more peaceful option and start construction of a new village.",
"village_elder_settlement_6",
[]],
[anyone|plyr, "village_elder_settlement_6", 
[], "Tell me more about a new castle",
"village_elder_settlement_castle",
[]],
[anyone|plyr, "village_elder_settlement_6", 
[], "Tell me more about a new village",
"village_elder_settlement_village",
[]],
[anyone|plyr, "village_elder_settlement_6", 
[], "You people are crazy. Leave!",
"village_elder_pretalk",
[]],
[anyone, "village_elder_settlement_castle", 
[], "You wish to increase the military presense of the {s2}?^\
Ressources required:^\
- 50 guards for protection and initial garrison^\
- 10 tools^\
- 2 Pickaxes^\
- 5 iron^\
- 25k ^\
Do you wish to proceed?",
"village_elder_settlement_castle_2",
[]],
[anyone|plyr, "village_elder_settlement_castle_2", 
[], "Yes",
"village_elder_settlement_castle_yes",
[]],
[anyone|plyr, "village_elder_settlement_castle_2", 
[], "No. Leave",
"village_elder_settlement_5",
[]],
[anyone|plyr, "village_elder_settlement_castle_yes", 
[], "Splendid. I'll leave you to it then.",
"village_elder_pretalk",
[]],

#End 
]

def modmerge(var_set):
    try:
        var_name_1 = "dialogs"
        orig_dialogs = var_set[var_name_1]
        modmerge_dialogs(orig_dialogs)
    except KeyError:
        errstring = "Variable set does not contain expected variable: "%s"." % var_name_1
        raise ValueError(errstring)
      
def modmerge_dialogs(orig_dialogs):
    try:
        # Add dialogs to the top of the list
        orig_dialogs.reverse() # Reverse list
        orig_dialogs  = dialogs_insert_block # add a new code
        orig_dialogs.reverse() # revers the list back
    except:
        import sys
        print "Injecton 1 failed:", sys.exc_info()[1]
        raise
