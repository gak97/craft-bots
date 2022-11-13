from cgitb import handler
from collections.abc import Set
import site
from typing import List, Tuple, Union
import requests
from random import randrange
import sys
# sys.path.append('./')
from agents.space_handler import SpaceHandler

class PDDLInterface:

    COLOURS = ['red', 'blue', 'orange', 'black', 'green']
    ACTIONS = ['move', 'mine', 'pick-up', 'drop', 'start-building', 'deposit', 'complete-building']

    @staticmethod
    # Function to write a problem file
    # Complete this function

    def writeProblem(world_info, file="agents/problem-temporal.pddl"):
        # Function that will write the problem file
        # write a simple config that will create 10 randomly generated nodes, and 6 fixed tasks (again, randomly generated).
        # Each task will require a different number of resources to solve

        handler = SpaceHandler()
        print('Writing problem file')
        with open(file, "w") as f:

            f.write("(define(problem craft-bots-temporal-problem)" + handler.newline)
            f.write(handler.newline)
            f.write("(:domain craft-bots-temporal)" + handler.newline)
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
            # take the maximum number of resources from the tasks
            max_resources = 0
            for task in world_info['tasks'].values():
                if sum(task['needed_resources']) > max_resources:
                    max_resources = sum(task['needed_resources'])
            for i in range(max_resources):
                f.write('r' + str(i) + handler.space)
            f.write(handler.dash + handler.space + 'resource' + handler.newline)

            f.write(handler.tab)
            for i in PDDLInterface.COLOURS:
                f.write(str(i) + handler.space)
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
                f.write(handler.tab)
                f.write('(mine_color m' + str(mine['id']) + handler.space + PDDLInterface.COLOURS[mine['colour']] + ')' + handler.newline)

            # set the variables create_site, not_created_site, mining, not_mining, carrying, not_carrying
            # deposited, not_deposited, constructed, not_constructed, rcolor
            f.write(handler.newline)
            for task in world_info['tasks'].values():
                for actor in world_info['actors'].values():      
                    for idx, j in enumerate(PDDLInterface.COLOURS):
                        f.write(handler.tab)
                        f.write('(not (carrying a' + str(actor['id']) + handler.space + str(j) + '))' + handler.newline)
                        f.write(handler.tab)
                        f.write('(not_carrying a' + str(actor['id']) + handler.space + str(j) + ')' + handler.newline)
                    f.write(handler.newline)
                f.write(handler.newline)
                break

            for task in world_info['tasks'].values():
                for actor in world_info['actors'].values():
                    for idx, j in enumerate(PDDLInterface.COLOURS):
                        f.write(handler.tab)
                        f.write('(not (deposited a' + str(actor['id']) + handler.space + str(j) + handler.space + 'n' + str(task['node']) + '))' + handler.newline)
                        f.write(handler.tab)
                        f.write('(not_deposited a' + str(actor['id']) + handler.space + str(j) + handler.space + 'n' + str(task['node']) + ')' + handler.newline)
                        # break
                    f.write(handler.newline)
                    # break
                f.write(handler.newline)
                break
                        
            for task in world_info['tasks'].values():
                f.write(handler.tab)
                f.write('(not (create_site' + handler.space + 'n' + str(task['node']) + '))' + handler.newline)
                f.write(handler.tab)
                f.write('(not_created_site' + handler.space + 'n' + str(task['node']) + ')' + handler.newline)
                break

            for task in world_info['tasks'].values():
                for idx, j in enumerate(PDDLInterface.COLOURS):
                    num_needed = task['needed_resources'][idx]
                    if num_needed > 0:
                        # (= (color_count c l) 0)
                        f.write(handler.tab)
                        f.write('(= (color_count' + handler.space + str(j) + handler.space + 'n' + str(task['node']) + ')' + handler.space + str(num_needed) + ')' + handler.newline)
                        # break
                    # break
                break

            # edge length
            # for edge in world_info['edges'].values():
            #     f.write(handler.tab)
            #     f.write('(= (edge_length' + handler.space + 'n' + str(edge['node_a']) + handler.space + 'n' + str(edge['node_b']) + ')' + handler.space + str(edge['length']) + ')' + handler.newline)

            # blue resource takes twice as long to mine
            blue_resource = PDDLInterface.COLOURS.index('blue')
            orange_resource = PDDLInterface.COLOURS.index('orange')
            for mine in world_info['mines'].values():
                color_id = mine['colour']
                if color_id == blue_resource:
                    f.write(handler.tab)
                    f.write('(= (mine_duration_blue' + handler.space + 'm' + str(mine['id']) + ')' + handler.space + str(33 * 2) + ')' + handler.newline)
                elif color_id == orange_resource:
                    f.write(handler.tab)
                    f.write('(= (mine_duration_orange' + handler.space + 'm' + str(mine['id']) + ')' + handler.space + str(33) + ')' + handler.newline)
                else:
                    f.write(handler.tab)
                    f.write('(= (mine_duration' + handler.space + 'm' + str(mine['id']) + ')' + handler.space + str(33) + ')' + handler.newline)

            # red resource can only be collected within time interval 0-1200
            # red_resource = PDDLInterface.COLOURS.index('red')
            # for task in world_info['tasks'].values():
            #     color_id = task['colour']
            #     if color_id == red_resource:
            #         f.write(handler.tab)
            #         f.write('= (collect_duration' + handler.space + 'n' + str(task['node']) + ')' + str(randrange(1200)) + handler.newline)
            #     else:
            #         f.write(handler.tab)
            #         f.write('= (collect_duration' + handler.space + 'n' + str(task['node']) + ')' + str(1) + handler.newline)

            # orange resource requires multiple actors to mine it
            # orange_resource = PDDLInterface.COLOURS.index('orange')
            # for mine in world_info['mines'].values():
            #     color_id = mine['colour']
            #     for actor in world_info['actors'].values():
            #         if actor['node'] == mine['node']:
            #             if color_id == orange_resource:
            #                 f.write(handler.tab)
            #                 f.write('= (mine_duration' + handler.space + 'm' + str(mine['id']) + ')' + str(33) + handler.newline)
            #             else:
            #                 f.write(handler.tab)
            #                 f.write('= (mine_duration' + handler.space + 'm' + str(mine['id']) + ')' + str(33) + handler.newline)

            # actor move speed
            # for actor in world_info['actors'].values():
            #     f.write(handler.tab)
            #     f.write('(= (move_speed' + handler.space + 'a' + str(actor['id']) + ')' + handler.space + str(5) + ')' + handler.newline)

            # actor build speed
            # for actor in world_info['actors'].values():
            #     f.write(handler.tab)
            #     f.write('(= (build_speed' + handler.space + 'a' + str(actor['id']) + ')' + handler.space + str(3) + ')' + handler.newline)

            # site progress
            # for task in world_info['tasks'].values():
            #     for actor in world_info['actors'].values():
            #         if actor['node'] == task['site']:
            #             f.write(handler.tab)
            #             f.write('(= (site_progress' + handler.space + 'n' + str(task['site']) + ')' + handler.space + str(100 - actor['progress']) + ')' + handler.newline)
            #             break

            f.write(handler.close_paren)
            f.write(handler.newline)
            f.write(handler.open_paren)

        ######################################################## GOAL ########################################################

            f.write(":goal" + handler.newline)
            f.write(handler.tab + '(and' + handler.newline)

            # fetch the tasks from the world info
            for task in world_info['tasks'].values():
                if not world_info['tasks'][task['id']]['completed']:
                    for idx, j in enumerate(PDDLInterface.COLOURS):
                        num_needed = task['needed_resources'][idx]
                        if num_needed > 0:
                            f.write(handler.tab + handler.tab)
                            f.write('(= (color_count' + handler.space + str(j) + handler.space + 'n' + str(task['node']) + ')' + handler.space + str(0) + ')' + handler.newline)
                            # break
                        # break
                    # break

            # for task in world_info['tasks'].values():
            #     for actor in world_info['actors'].values():
            #         if actor['node'] != task['node']:
            #             f.write(handler.tab + handler.tab)
            #             f.write('(alocation a' + str(actor['id']) + ' n' + str(task['node']) + ')' + handler.newline)
            #     break

            # for task in world_info['tasks'].values():
            #     f.write(handler.tab + handler.tab)
            #     f.write('(create_site' + handler.space + 'n' + str(task['node']) + ')' + handler.newline)

            # for mine in world_info['mines'].values():
            #     f.write(handler.tab + handler.tab)
            #     f.write('(rlocation' + handler.space + 'n' + str(mine['node']) + handler.space + PDDLInterface.COLOURS[mine['colour']] + ')' + handler.newline)

            # for actor in world_info['actors'].values():
            #     for mine in world_info['mines'].values():
            #         if actor['node'] == mine['node']:
            #             f.write(handler.tab + handler.tab)
            #             f.write('(carrying' + handler.space + 'a' + str(actor['id']) + handler.space + PDDLInterface.COLOURS[mine['colour']] + ')' + handler.newline)

            # for task in world_info['tasks'].values():
            #     for actor in world_info['actors'].values():
            #         for idx, j in enumerate(PDDLInterface.COLOURS):
            #             f.write(handler.tab + handler.tab)
            #             f.write('(deposited a' + str(actor['id']) + handler.space + str(j) + handler.space + 'n' + str(task['node']) + ')' + handler.newline)

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
    PDDLInterface.generatePlan("domain-craft-bots-temporal.pddl", "problem-temporal.pddl", "plan-temporal.pddl", verbose=True)
    plan = PDDLInterface.readPDDLPlan('plan-temporal.pddl')
    print(plan)