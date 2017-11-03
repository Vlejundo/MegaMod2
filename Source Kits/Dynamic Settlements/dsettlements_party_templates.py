from header_common import *
from header_parties import *
from ID_troops import *
from ID_factions import *
from ID_map_icons import *


####################################################################################################################
#  Each party template record contains the following fields:
#  1) Party-template id: used for referencing party-templates in other files.
#     The prefix pt_ is automatically added before each party-template id.
#  2) Party-template name.
#  3) Party flags. See header_parties.py for a list of available flags
#  4) Menu. ID of the menu to use when this party is met. The value 0 uses the default party encounter system.
#  5) Faction
#  6) Personality. See header_parties.py for an explanation of personality flags.
#  7) List of stacks. Each stack record is a tuple that contains the following fields:
#    7.1) Troop-id. 
#    7.2) Minimum number of troops in the stack. 
#    7.3) Maximum number of troops in the stack. 
#    7.4) Member flags(optional). Use pmf_is_prisoner to note that this member is a prisoner.
#     Note: There can be at most 6 stacks.
####################################################################################################################


party_templates = [

("construction_site"				,"Construction"							,icon_camp_tent|pf_is_static																		,0		,fac_neutral		,merchant_personality			,[(trp_looter_leader,1,1)]),
("town_runaways"					,"Townsfolk"							,icon_people_peasant|pf_civilian																	,0		,fac_innocents		,merchant_personality			,[(trp_mercenary_e_farmer,5,20),(trp_woman_e_peasant,3,16)]),

#End
]