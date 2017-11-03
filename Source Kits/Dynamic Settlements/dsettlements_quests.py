from header_quests import *
####################################################################################################################
#  Each quest record contains the following fields:
#  1) Quest id: used for referencing quests in other files. The prefix qst_ is automatically added before each quest-id.
#  2) Quest Name: Name displayed in the quest screen.
#  3) Quest flags. See header_quests.py for a list of available flags
#  4) Quest Description: Description displayed in the quest screen.
#
# Note that you may call the opcode setup_quest_text for setting up the name and description
####################################################################################################################

quests = [
("construct_settlement", "Settlements: Visit {s13}", qf_random_quest, # str_store_party_name_link for s13
"{!} The village elder in {s13} wants to speak to you about possible construction options regarding the settlement."),

#End
]