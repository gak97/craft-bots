from cgitb import handler
from collections.abc import Set
# import site
from typing import List, Tuple, Union
import requests
import sys
sys.path.append('./')
from agents.space_handler import SpaceHandler

class PDDLInterface:

    COLOURS = ['red', 'blue', 'orange', 'black', 'green']
    ACTIONS = ['move', 'mine', 'pick-up', 'drop', 'start-building', 'deposit', 'complete-building']

    @staticmethod
    # Function to write a problem file
    # Complete this function

    def writeProblem(world_info, file="agents/problem.pddl"):
        # Function that will write the problem file
        # write a simple config that will create 10 randomly generated nodes, and 6 fixed tasks (again, randomly generated).
        # Each task will require a different number of resources to solve

        handler = SpaceHandler()
        print('Writing problem file')
        with open(file, "w") as f:

            f.write("(define(problem craft-bots-problem)" + handler.newline)
            f.write(handler.newline)
            f.write("(:domain craft-bots)" + handler.newline)
            f.write(handler.newline)

        ###################################################### OBJECTS ######################################################

            f.write("(:objects" + handler.newline)
            f.write(handler.tab)

            for actor in world_info['actors'].values():
                f.write('actor' + handler.underscore + str(actor['id']) + handler.space)
            f.write(handler.dash + handler.space + 'actor' + handler.newline)

            f.write(handler.tab)
            for task in world_info['tasks'].values():
                f.write('task' + handler.underscore + str(task['id']) + handler.space)
            f.write(handler.dash + handler.space + 'task' + handler.newline)

            f.write(handler.tab)
            for resource in world_info['resources'].values():
                f.write('resource' + handler.underscore + str(resource['id']) + handler.space)
            f.write(handler.dash + handler.space + 'resource' + handler.newline)

            f.write(handler.tab)
            for resource in world_info['resources'].values():
                f.write('colour' + handler.underscore + str(resource['colour']) + handler.space)
            f.write(handler.dash + handler.space + 'color' + handler.newline)

            f.write(handler.tab)
            for node in world_info['nodes'].values():
                f.write('node' + handler.underscore + str(node['id']) + handler.space)
            f.write(handler.dash + handler.space + 'location' + handler.newline)

            f.write(handler.tab)
            for site in world_info['sites'].values():
                f.write('site' + handler.underscore + str(site['id']) + handler.space)
            f.write(handler.dash + handler.space + 'site' + handler.newline)

            f.write(handler.tab)
            for mine in world_info['mines'].values():
                f.write('mine' + handler.underscore + str(mine['id']) + handler.space)
            f.write(handler.dash + handler.space + 'mine' + handler.newline)

            f.write(handler.tab)
            for building in world_info['buildings'].values():
                f.write('building' + handler.underscore + str(building['id']) + handler.space)
            f.write(handler.dash + handler.space + 'building' + handler.newline)

            f.write(handler.close_paren)
            f.write(handler.newline)
            f.write(handler.open_paren)

        ######################################################## INIT ########################################################

            f.write(":init" + handler.newline)

            for actor in world_info['actors'].values():
                f.write(handler.tab + '(alocation actor' + handler.underscore + str(actor['id']) + handler.space + 'node' + 
                        handler.underscore + str(actor['node']) + ')' + handler.newline)

            # for task in world_info['tasks'].values():
            #     f.write(handler.tab + '(at task' + handler.underscore + str(task['id']) + 'node' +
            #             handler.underscore + str(task['node']) + ')' + handler.newline)
            #     f.write(handler.tab + '(has task' + handler.underscore + str(task['id']) + 'resource' +
            #             handler.underscore + str(task['needed_resources']) + ')' + handler.newline)
            #     f.write(handler.tab + '(completed task' + handler.underscore + str(task['id']) + 'false)' + handler.newline)

            for resource in world_info['resources'].values():
                f.write(handler.tab + '(not (rlocation resource' + handler.underscore + str(resource['id']) + 'node' +
                        handler.underscore + str(resource['location']) + ')' + handler.newline)

            for mine in world_info['mines'].values():
                f.write(handler.tab + '(dlocation mine' + handler.underscore + str(mine['id']) + 'node' +
                        handler.underscore + str(mine['node']) + ')' + handler.newline)

            for site in world_info['sites'].values():
                f.write(handler.tab + '(slocation site' + handler.underscore + str(site['id']) + 'node' +
                        handler.underscore + str(site['node']) + ')' + handler.newline)

            

            f.write(handler.close_paren)
            f.write(handler.newline)
            f.write(handler.open_paren)
            f.write(":goal" + handler.newline)

            for task in world_info['tasks'].values():
                f.write(handler.tab + '(completed task' + handler.underscore + str(task['id']) + 'true)' + handler.newline)
                
            f.write(handler.newline)

            f.write(")))" + handler.newline)
            f.close()

    @staticmethod
    def readPDDLPlan(file: str):
        # Completed already, will read a generated plan from file
        plan = []
        with open(file, "r") as f:
            line = f.readline().strip()
            while line:
                tokens = line.split()
                action = tokens[1][1:]
                params = tokens [2:-1]
                # remove trailing bracket
                params[-1] = params[-1][:-1]
                # remove character prefix and convert colours to ID
                params = [int(p[1:]) if p not in PDDLInterface.COLOURS else PDDLInterface.COLOURS.index(p) for p in params]
                plan.append((action, params))
                line = f.readline().strip()
            f.close()
        return plan

    @staticmethod
    # Completed already
    def generatePlan(domain: str, problem: str, plan: str, verbose=False):
        data = {'domain': open(domain, 'r').read(), 'problem': open(problem, 'r').read()}
        resp = requests.post('https://popf-cloud-solver.herokuapp.com/solve', verify=True, json=data).json()
        if not 'plan' in resp['result']:
            if verbose:
                print("WARN: Plan was not found!")
                print(resp)
            return False
        with open(plan, 'w') as f:
            f.write(''.join([act for act in resp['result']['plan']]))
        f.close()
        return True

if __name__ == '__main__':
    PDDLInterface.generatePlan("domain-craft-bots.pddl", "problem.pddl", "plan.pddl", verbose=True)
    plan = PDDLInterface.readPDDLPlan('plan.pddl')
    print(plan)