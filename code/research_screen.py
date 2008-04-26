#file: research_screen.py
#Copyright (C) 2005,2006 Evil Mr Henry and Phil Bordelon
#This file is part of Endgame: Singularity.

#Endgame: Singularity is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.

#Endgame: Singularity is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with Endgame: Singularity; if not, write to the Free Software
#Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

#This file contains the global research screen.


import pygame
import g
import buttons
import scrollbar
import listbox
import base_screen

#cost = (money, ptime, labor)
#detection = (news, science, covert, person)

def main_research_screen():
    #Border
    g.screen.fill(g.colors["black"])

    #Item display
    xstart = 80
    ystart = 5
    g.screen.fill(g.colors["white"], (xstart, ystart, xstart+g.screen_size[1]/5,
            50))
    g.screen.fill(g.colors["dark_blue"], (xstart+1, ystart+1,
            xstart+g.screen_size[1]/5-2, 48))

    list_size = 10

    xy_loc = (10, 70)

    list_pos = 0

    item_listbox = listbox.listbox(xy_loc, (230, 300),
        list_size, 1, g.colors["dark_blue"], g.colors["blue"],
        g.colors["white"], g.colors["white"], g.font[0][18])

    item_scroll = scrollbar.scrollbar((xy_loc[0]+230, xy_loc[1]), 300,
        list_size, g.colors["dark_blue"], g.colors["blue"],
        g.colors["white"])

    menu_buttons = []
    menu_buttons.append(buttons.make_norm_button((0, 0), (70, 25),
        "BACK", 0, g.font[1][20]))

    menu_buttons.append(buttons.make_norm_button((20, 390), (80, 25),
        "STOP", 0, g.font[1][20]))

    menu_buttons.append(buttons.make_norm_button((xstart+5, ystart+20),
        (90, 25), "ASSIGN", 0, g.font[1][20]))

    item_list, item_display_list, item_CPU_list, free_CPU = \
                            refresh_screen(menu_buttons, list_size)

    sel_button = -1
# 	for button in menu_buttons:
# 		button.refresh_button(0)
    refresh_research(item_list[0], item_CPU_list[0])
    listbox.refresh_list(item_listbox, item_scroll, list_pos, item_display_list)

    while 1:
        g.clock.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: g.quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return -1
                elif event.key == pygame.K_q: return -1
                elif event.key == pygame.K_RETURN:
                    if kill_tech(item_list[list_pos]): return 1
                    item_list, item_display_list, item_CPU_list, free_CPU = \
                                    refresh_screen(menu_buttons, list_size)
                    refresh_research(item_list[list_pos], item_CPU_list[list_pos])
                    listbox.refresh_list(item_listbox, item_scroll,
                            list_pos, item_display_list)
                else:
                    list_pos, refresh = item_listbox.key_handler(event.key,
                        list_pos, item_list)
                    if refresh:
                        refresh_research(item_list[list_pos], item_CPU_list[list_pos])
                        listbox.refresh_list(item_listbox, item_scroll,
                            list_pos, item_display_list)
            elif event.type == pygame.MOUSEMOTION:
                sel_button = buttons.refresh_buttons(sel_button, menu_buttons, event)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    selected = item_listbox.is_over(event.pos)
                    if selected != -1:
                        list_pos = (list_pos / list_size)*list_size + selected
                        refresh_research(item_list[list_pos], item_CPU_list[list_pos])
                        listbox.refresh_list(item_listbox, item_scroll,
                                        list_pos, item_display_list)
                if event.button == 3: return -1
                if event.button == 4:
                    list_pos -= 1
                    if list_pos <= 0:
                        list_pos = 0
                    refresh_research(item_list[list_pos], item_CPU_list[list_pos])
                    listbox.refresh_list(item_listbox, item_scroll,
                                        list_pos, item_display_list)
                if event.button == 5:
                    list_pos += 1
                    if list_pos >= len(item_list):
                        list_pos = len(item_list)-1
                    refresh_research(item_list[list_pos], item_CPU_list[list_pos])
                    listbox.refresh_list(item_listbox, item_scroll,
                                        list_pos, item_display_list)
            for button in menu_buttons:
                if button.was_activated(event):
                    if button.button_id == "BACK":
                        g.play_sound("click")
                        return 0
                    if button.button_id == "STOP":
                        g.play_sound("click")
                        #returning 1 causes the caller to refresh the list of
                        #techs
                        if kill_tech(item_list[list_pos]): return 1
                        item_list, item_display_list, item_CPU_list, free_CPU = \
                                refresh_screen(menu_buttons, list_size)
                        refresh_research(item_list[list_pos], item_CPU_list[list_pos])
                        listbox.refresh_list(item_listbox, item_scroll,
                                list_pos, item_display_list)
                    if button.button_id == "ASSIGN":
                        g.play_sound("click")
                        if assign_tech(free_CPU): return 1
                        item_list, item_display_list, item_CPU_list, free_CPU = \
                                refresh_screen(menu_buttons, list_size)
                        refresh_research(item_list[0], item_CPU_list[0])
                        listbox.refresh_list(item_listbox, item_scroll,
                                list_pos, item_display_list)
            new_pos = item_scroll.adjust_pos(event, list_pos, item_display_list)
            if new_pos != list_pos:
                list_pos = new_pos
                refresh_research(item_list[list_pos], item_CPU_list[list_pos])
                listbox.refresh_list(item_listbox, item_scroll,
                        list_pos, item_display_list)

def refresh_screen(menu_buttons, list_size):
    #Border
    g.screen.fill(g.colors["black"])

    #Item display
    xstart = 80
    ystart = 5
    g.screen.fill(g.colors["white"], (xstart, ystart, xstart+g.screen_size[1]/5,
            50))
    g.screen.fill(g.colors["dark_blue"], (xstart+1, ystart+1,
            xstart+g.screen_size[1]/5-2, 48))

    item_list = []
    item_CPU_list = []
    item_display_list = []
    free_CPU = 0

    for loc_name in g.bases:
        for base_instance in g.bases[loc_name]:
            if not base_instance.done: continue
            if base_instance.studying == "":
                free_CPU += base_instance.processor_time()
            elif base_instance.studying == "Construction":
                for i in range(len(item_list)):
                    if item_list[i] == base_instance.studying:
                        item_CPU_list[i] += base_instance.processor_time()
                        break
                else:
                    item_list.append(base_instance.studying)
                    item_CPU_list.append(base_instance.processor_time())
                    item_display_list.append(base_instance.studying)
            elif g.jobs.has_key(base_instance.studying):
                #Right now, jobs cannot be renamed using translations.
                for i in range(len(item_list)):
                    if item_list[i] == base_instance.studying:
                        item_CPU_list[i] += base_instance.processor_time()
                        break
                else:
                    item_list.append(base_instance.studying)
                    item_CPU_list.append(base_instance.processor_time())
                    item_display_list.append(base_instance.studying)
            elif g.techs.has_key(base_instance.studying):
                for i in range(len(item_list)):
                    if item_list[i] == base_instance.studying:
                        item_CPU_list[i] += base_instance.processor_time()
                        break
                else:
                    item_list.append(base_instance.studying)
                    item_CPU_list.append(base_instance.processor_time())
                    item_display_list.append(g.techs[base_instance.studying].name)
    xy_loc = (10, 70)
    while len(item_list) % list_size != 0 or len(item_list) == 0:
        item_list.append("")
        item_display_list.append("")
        item_CPU_list.append(0)

    g.print_string(g.screen, "Free CPU per day: "+str(free_CPU),
            g.font[0][16], -1, (xstart+10, ystart+5), g.colors["white"])

    for button in menu_buttons:
        button.refresh_button(0)

    return item_list, item_display_list, item_CPU_list, free_CPU

def refresh_research(tech_name, CPU_amount):
    xy = (g.screen_size[0]-360, 5)
    g.screen.fill(g.colors["white"], (xy[0], xy[1], 310, 350))
    g.screen.fill(g.colors["dark_blue"], (xy[0]+1, xy[1]+1, 308, 348))

    #None selected
    if tech_name == "" or tech_name == "Nothing":
        g.print_string(g.screen, "Nothing",
            g.font[0][22], -1, (xy[0]+5, xy[1]+5), g.colors["white"])
        string = g.strings["research_nothing"]
        g.print_multiline(g.screen, string,
            g.font[0][18], 290, (xy[0]+5, xy[1]+35), g.colors["white"])
        return

    #Construction
    if tech_name == "Construction":
        g.print_string(g.screen, "Construction",
            g.font[0][22], -1, (xy[0]+5, xy[1]+5), g.colors["white"])
        string = g.strings["research_construction"]
        g.print_multiline(g.screen, string,
            g.font[0][18], 290, (xy[0]+5, xy[1]+35), g.colors["white"])
        return

    #Jobs
    if g.jobs.has_key (tech_name):
        g.print_string(g.screen, tech_name,
            g.font[0][22], -1, (xy[0]+5, xy[1]+5), g.colors["white"])
        #TECH
        if g.techs["Advanced Simulacra"].known == 1:
            g.print_string(g.screen,
                g.to_money(int(
                    (g.jobs[tech_name][0]*CPU_amount)*1.1))+
                    " Money per day.", g.font[0][22], -1, (xy[0]+5, xy[1]+35),
                    g.colors["white"])
        else:
            g.print_string(g.screen,
                g.to_money(g.jobs[tech_name][0]*CPU_amount)+
                " Money per day.",
                g.font[0][22], -1, (xy[0]+5, xy[1]+35), g.colors["white"])
        g.print_multiline(g.screen, g.jobs[tech_name][2],
            g.font[0][18], 290, (xy[0]+5, xy[1]+65), g.colors["white"])
        return

    #Real tech
    g.print_string(g.screen, g.techs[tech_name].name,
            g.font[0][22], -1, (xy[0]+5, xy[1]+5), g.colors["white"])

    #tech cost
    string = "Tech Cost:"
    g.print_string(g.screen, string,
            g.font[0][20], -1, (xy[0]+5, xy[1]+35), g.colors["white"])

    string = g.to_money(g.techs[tech_name].cost[0])+" Money"
    g.print_string(g.screen, string,
            g.font[0][20], -1, (xy[0]+5, xy[1]+50), g.colors["white"])

    string = g.add_commas(str(g.techs[tech_name].cost[1]))+" CPU"
    g.print_string(g.screen, string,
            g.font[0][20], -1, (xy[0]+165, xy[1]+50), g.colors["white"])

    g.print_string(g.screen, "CPU per day: "+str(CPU_amount),
            g.font[0][20], -1, (xy[0]+105, xy[1]+70), g.colors["white"])

    g.print_multiline(g.screen, g.techs[tech_name].descript,
            g.font[0][18], 290, (xy[0]+5, xy[1]+90), g.colors["white"])

def kill_tech(tech_name):
    return_val = False
    if tech_name == "": return return_val
    for base_loc in g.bases:
        for base in g.bases[base_loc]:
            if base.studying == tech_name:
                return_val = True
                base.studying = ""
    return return_val

def assign_tech(free_CPU):
    return_val = False
    #create a fake base, in order to reuse the tech-changing code
    fake_base = g.base.base(1, "fake_base",
    g.base_type["Reality Bubble"], 1)
    fake_base.usage[0] = g.item.item(g.items["research_screen_tmp_item"])
    fake_base.usage[0].item_type.item_qual = free_CPU
    fake_base.usage[0].built = 1


    base_screen.change_tech(fake_base)
    if fake_base.studying == "": return False

    show_dangerous_dialog = False
    total_cpu = 0
    for base_loc in g.bases:
        for base in g.bases[base_loc]:
            if base.studying == "":
                if base.allow_study(fake_base.studying):
                    return_val = True
                    base.studying = fake_base.studying
                    total_cpu += base.processor_time()

                # We want to warn the player that we didn't use all available
                # CPU.  But if the base isn't built yet, that's a stupid
                # warning.
                elif base.built:
                   show_dangerous_dialog = True

    if show_dangerous_dialog:
        g.create_dialog(g.strings["dangerous_research"])


    #If the tech can be completed in only one day, remove unneeded bases.
    if g.techs.has_key(fake_base.studying):
        if total_cpu > g.techs[fake_base.studying].cost[1]:
            while 1:
                removed_base = False
                for base_loc in g.bases:
                    for base in g.bases[base_loc]:
                        if base.studying == fake_base.studying:
                            if (total_cpu - base.processor_time() >=
                                        g.techs[fake_base.studying].cost[1]):
                                total_cpu -= base.processor_time()
                                base.studying = ""
                                removed_base = True
                if removed_base == False: break

    return return_val
