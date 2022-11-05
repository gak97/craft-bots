from cgitb import handler
from collections.abc import Set
# import site
import random
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
                f.write('a' + str(actor['id']) + handler.space)
            f.write(handler.dash + handler.space + 'actor' + handler.newline)

            f.write(handler.tab)
            for task in world_info['tasks'].values():
                f.write('t' + str(task['id']) + handler.space)
            f.write(handler.dash + handler.space + 'task' + handler.newline)

            f.write(handler.tab)
            for node in world_info['nodes'].values():
                f.write('n' + str(node['id']) + handler.space)
            f.write(handler.dash + handler.space + 'location' + handler.newline)

            f.write(handler.tab)
            for mine in world_info['mines'].values():
                f.write('m' + str(mine['id']) + handler.space)
            f.write(handler.dash + handler.space + 'mine' + handler.newline)

            f.write(handler.tab)
            for task in world_info['tasks'].values():
                for i in range(sum(task['needed_resources'])):
                    f.write('r' + str(i) + handler.space)
                break
            f.write(handler.dash + handler.space + 'resource' + handler.newline)

            f.write(handler.tab)
            for i in range(len(PDDLInterface.COLOURS)):
                f.write('c' + str(i) + handler.space)
            f.write(handler.dash + handler.space + 'color' + handler.newline)

            f.write(handler.close_paren)
            f.write(handler.newline)
            f.write(handler.open_paren)

        ######################################################## INIT ########################################################

            f.write(":init" + handler.newline)

            # set the initial node for each actor and negate the rest of the nodes
            for actor in world_info['actors'].values():
                f.write(handler.tab)
                f.write('(alocation a' + str(actor['id']) + handler.space + 'n' + str(actor['node']) + ')' + handler.newline)
                for node in world_info['nodes'].values():
                    if node['id'] != actor['node']:
                        f.write(handler.tab)
                        f.write('(not (alocation a' + str(actor['id']) + handler.space + 'n' + str(node['id']) + '))' + handler.newline)

            # set the connected nodes given the edges
            f.write(handler.newline)
            for edge in world_info['edges'].values():
                f.write(handler.tab)
                f.write('(connected n' + str(edge['node_a']) + handler.space + 'n' + str(edge['node_b']) + ')')
                f.write(handler.tab)
                f.write('(connected n' + str(edge['node_b']) + handler.space + 'n' + str(edge['node_a']) + ')')
                f.write(handler.newline)

            # set the initial dig location for the mines
            f.write(handler.newline)
            for mine in world_info['mines'].values():
                f.write(handler.tab)
                f.write('(dlocation m' + str(mine['id']) + handler.space + 'n' + str(mine['node']) + ')' + handler.newline)

            # set the variables create_site, not_created_site, mining, not_mining, carrying, not_carrying
            # deposited, not_deposited, constructed, not_constructed, rcolor
            f.write(handler.newline)
            for task in world_info['tasks'].values():
                for i in range(sum(task['needed_resources'])):
                    for actor in world_info['actors'].values():
                        f.write(handler.tab)
                        f.write('(not (create_site a' + str(actor['id']) + handler.space + 'n' + str(task['node']) + '))' + handler.newline)
                        f.write(handler.tab)
                        f.write('(not_created_site a' + str(actor['id']) + handler.space + 'n' + str(task['node']) + ')' + handler.newline)
                        f.write(handler.tab)
                        f.write('(not (mining a' + str(actor['id']) + handler.space + 'r' + str(i) + '))' + handler.newline)
                        f.write(handler.tab)
                        f.write('(not_mining a' + str(actor['id']) + handler.space + 'r' + str(i) + ')' + handler.newline)
                        f.write(handler.tab)
                        f.write('(not (carrying a' + str(actor['id']) + handler.space + 'r' + str(i) + '))' + handler.newline)
                        f.write(handler.tab)
                        f.write('(not_carrying a' + str(actor['id']) + handler.space + 'r' + str(i) + ')' + handler.newline)
                        
                        for j in range(len(PDDLInterface.COLOURS)):
                            f.write(handler.tab)
                            f.write('(not (deposited a' + str(actor['id']) + handler.space + 'r' + str(i) + handler.space + 'c' + str(j) + handler.space + 'n' + str(task['node']) + '))' + handler.newline)
                            f.write(handler.tab)
                            f.write('(not_deposited a' + str(actor['id']) + handler.space + 'r' + str(i) + handler.space + 'c' + str(j) + handler.space + 'n' + str(task['node']) + ')' + handler.newline)
                            f.write(handler.tab)
                            f.write('(not (constructed a' + str(actor['id']) + handler.space + 'r' + str(i) + handler.space + 'c' + str(j) + handler.space + 'n' + str(task['node']) + '))' + handler.newline)
                            f.write(handler.tab)
                            f.write('(not_constructed a' + str(actor['id']) + handler.space + 'r' + str(i) + handler.space + 'c' + str(j) + handler.space + 'n' + str(task['node']) + ')' + handler.newline)
                            f.write(handler.tab)
                            f.write('(rcolor r' + str(i) + handler.space + 'c' + str(j) + ')' + handler.newline)
                            break
                        break
                    break 
                break

            f.write(handler.close_paren)
            f.write(handler.newline)
            f.write(handler.open_paren)

        ######################################################## GOAL ########################################################

            f.write(":goal" + handler.newline)
            f.write(handler.tab + '(and' + handler.newline)

            # set the goal node for each actor different from the initial node
            # for actor in world_info['actors'].values():
            #     for node in world_info['nodes'].values():
            #         if node['id'] != actor['node']:
            #             f.write(handler.tab + handler.tab)
            #             f.write('(alocation a' + str(actor['id']) + handler.space + 'n' + str(node['id']) + ')' + handler.newline)
            #             break

            # set the goal node for digging for each actor with different resource
            # for actor in world_info['actors'].values():
            #     for resource in world_info['resources'].values():
            #         if resource['id'] != actor['resources']:
            #             f.write(handler.tab + handler.tab)
            #             f.write('(rlocation r' + str(resource['id']) + handler.space + 'n' + str(actor['node']) + ')' + handler.newline)
            #             break

            # fetch the tasks from the world info
            for task in world_info['tasks'].values():
                for i in range(len(task['needed_resources'])):
                    for actor in world_info['actors'].values():
                        for j in range(len(PDDLInterface.COLOURS)):
                            # f.write(handler.tab + handler.tab)
                            # f.write('(deposited a' + str(actor['id']) + handler.space + 'r' + str(i) + handler.space + 'c' + str(j) + handler.space + 'n' + str(task['node']) + ')' + handler.newline)
                            f.write(handler.tab + handler.tab)
                            f.write('(constructed a' + str(actor['id']) + handler.space + 'r' + str(i) + handler.space + 'c' + str(j) + handler.space + 'n' + str(task['node']) + ')' + handler.newline)
                        break
                    break
                break

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