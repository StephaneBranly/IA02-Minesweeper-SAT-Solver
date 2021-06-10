from pprint import pprint
from moteur.crocomine_client import CrocomineClient

def test():
    server = "http://localhost:8000"
    group = "Groupe 12"
    members = "Khaled et Sylvain"
    croco = CrocomineClient(server, group, members)

    status, msg, grid_infos = croco.new_grid()
    print(status, msg)
    pprint(grid_infos)

    status, msg, grid_infos = croco.new_grid()
    print(msg, status)
    pprint(grid_infos)

    status, msg, grid_infos = croco.new_grid()
    print(status, msg)
    pprint(grid_infos)

    status, msg, infos = croco.discover(6, 2)
    print(status, msg)
    pprint(infos)

if __name__ == "__main__":
    test()
