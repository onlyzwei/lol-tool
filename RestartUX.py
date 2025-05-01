from lcu_core import Lcu_core

Lcu_core = Lcu_core()

def restart():

	Lcu_core.lcu_request("POST", '/riotclient/kill-and-restart-ux','')
