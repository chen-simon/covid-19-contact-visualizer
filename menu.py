"""
Interface Module

This module contains the functions that are needed to for the interface. The gui allows the user to
adjust the variables for the prediction, then generate the graph.

This file is Copyright (c) 2020 Patricia Ding, Makayla Duffus, Simon Chen, Salman Husainie.
"""
import pygame
import pygame_gui
from typing import List
from simulation import Simulation
pygame.init()


def run_interface() -> None:
    """Runs the graphical user interface.
    """
    pygame.display.set_caption('Simulation Conditions')
    window_surface = pygame.display.set_mode((355, 365))

    background = pygame.Surface((355, 365))
    background.fill(pygame.Color('#CCCCCC'))

    manager = pygame_gui.UIManager((355, 365))

    # text boxes
    pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((25, 25), (200, 55)),
                                  html_text='Number of People: ', manager=manager)

    pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((25, 85), (200, 55)),
                                  html_text='Level of Closeness: ', manager=manager)

    pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((25, 145), (200, 55)),
                                  html_text='Starting Number of Infected: ', manager=manager)

    pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((25, 205), (200, 55)),
                                  html_text='Connected: ', manager=manager)

    # value boxes
    people_change = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((200, 25), (75, 55)),
                                                  html_text='20', manager=manager)

    closeness_change = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((200, 85), (75, 55)),
                                                     html_text='medium', manager=manager)

    infected_change = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((200, 145), (75, 55)),
                                                    html_text='1', manager=manager)

    connected_change = pygame_gui.elements.UITextBox(
        relative_rect=pygame.Rect((200, 205), (75, 55)),
        html_text='yes', manager=manager)

    # Plus Minus Buttons
    num_people_plus = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((280, 25), (50, 25)),
                                                   text='+', manager=manager)

    num_people_minus = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((280, 55), (50, 25)),
                                                    text='-', manager=manager)

    closeness_plus = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((280, 85), (50, 25)),
                                                  text='+', manager=manager)

    closeness_minus = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((280, 115), (50, 25)),
                                                   text='-', manager=manager)

    infected_plus = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((280, 145), (50, 25)),
                                                 text='+', manager=manager)

    infected_minus = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((280, 175), (50, 25)),
                                                  text='-', manager=manager)

    connected_plus = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((280, 205), (50, 25)),
                                                  text='+', manager=manager)

    connected_minus = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((280, 235), (50, 25)),
                                                   text='-', manager=manager)
    # Generate Button
    start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((25, 265), (305, 70)),
                                                text='Generate', manager=manager)

    clock = pygame.time.Clock()
    is_running = True

    variable_values = [20, 1, 1, 1]

    while is_running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    # Plus minus buttons
                    if event.ui_element == num_people_plus and variable_values[0] < 60:
                        change_interval(variable_values, people_change, 10, 0)

                    elif event.ui_element == num_people_minus and variable_values[0] > 10:
                        change_interval(variable_values, people_change, -10, 0)

                    elif event.ui_element == closeness_plus and variable_values[1] < 2:
                        change_interval(variable_values, closeness_change, 1, 1)

                    elif event.ui_element == closeness_minus and variable_values[1] > 0:
                        change_interval(variable_values, closeness_change, -1, 1)

                    elif event.ui_element == infected_plus \
                            and variable_values[2] < variable_values[0]:
                        change_interval(variable_values, infected_change, 1, 2)

                    elif event.ui_element == infected_minus and variable_values[2] > 0:
                        change_interval(variable_values, infected_change, -1, 2)

                    elif event.ui_element == connected_plus and variable_values[3] == 0:
                        change_interval(variable_values, connected_change, 1, 3)

                    elif event.ui_element == connected_minus and variable_values[3] == 1:
                        change_interval(variable_values, connected_change, -1, 3)

                    # Generate Button
                    elif event.ui_element == start_button:
                        sim = Simulation((variable_values[0],
                                          determine_step(1, variable_values[1]),
                                          variable_values[2],
                                          determine_step(3, variable_values[3])))
                        sim.run(21, with_degrees=True)

            manager.process_events(event)

        manager.update(time_delta)

        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)

        pygame.display.update()


def change_interval(variable_values: List[float], textbox, delta: float, dataset: int) -> None:
    """ Changes the value of the variable for the selected dataset by a given delta"""
    variable_values[dataset] += delta
    if dataset == 1 or dataset == 3:
        textbox.html_text = determine_step(dataset, int(variable_values[dataset]))

    else:
        value = str(variable_values[dataset])
        textbox.html_text = value

    textbox.rebuild()


def determine_step(dataset: int, variable_value: int) -> str:
    """Determine which step to display on the menu based on the given dataset"""
    if dataset == 1:
        if variable_value == 0:
            return 'low'
        elif variable_value == 1:
            return 'medium'
        elif variable_value == 2:
            return 'high'
    else:
        if variable_value == 0:
            return 'no'
        else:
            return 'yes'
