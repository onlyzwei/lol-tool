from lcu_core import Lcu_core

Lcu_core = Lcu_core()

def dodge():

	Lcu_core.lcu_request("POST", '/lol-login/v1/session/invoke?destination=lcdsServiceProxy&method=call&args=["","teambuilder-draft","quitV2",""]', "")
