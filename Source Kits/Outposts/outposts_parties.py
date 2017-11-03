#=#######################################
# Lumos: This file contains all the parties for the Outposts kit.
#        Place 'em in your module_parties.
#-#######################################
from module_parties import *

parties = [
#-## Outposts begin
  ("outpost_1","Outpost",icon_outpost|pf_disabled|pf_is_static|pf_always_visible|pf_label_small, no_menu, pt_none, fac_commoners,0,ai_bhvr_hold,0,(0, 0),[]),
  ("outpost_2","Outpost",icon_outpost|pf_disabled|pf_is_static|pf_always_visible|pf_label_small, no_menu, pt_none, fac_commoners,0,ai_bhvr_hold,0,(1, -1),[]),
  ("fort","Fort",icon_fort_a|pf_disabled|pf_is_static|pf_always_visible|pf_label_medium, no_menu, pt_none, fac_commoners,0,ai_bhvr_hold,0,(1, 1),[]),
#-## Outposts end
]


from util_wrappers import *
from util_common import *

def modmerge_parties(orig_parties, check_duplicates = False):
	try:
		find_i = list_find_first_match_i( orig_parties, "looter_spawn_point" )
		OpBlockWrapper(orig_parties).InsertBefore(find_i, parties)		
	except:
		import sys
		print "Injecton 1 failed:", sys.exc_info()[1]
		raise
	
# Used by modmerger framework version >= 200 to merge stuff
def modmerge(var_set):
    try:
        var_name_1 = "parties"
        orig_parties = var_set[var_name_1]
        modmerge_parties(orig_parties)
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)