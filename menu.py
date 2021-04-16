"""CSC111 Project: COVID-19 Contact Visualizer

Module Description
==================
Interface Module
This module contains the functions that are needed to for the interface. The gui allows the user to
adjust the variables for the prediction, then generate the graph.

This module is a modified version of the Endangered Species Predictor's interface from Simon,
Makayla, and Patricia's CSC110 Final Project.

Copyright and Usage Information
===============================
This file is Copyright (c) 2021 Simon Chen, Patricia Ding, Salman Husainie, Makayla Duffus
"""
import math

import pygame
import pygame_gui
from typing import List, Tuple
from simulation import Simulation
pygame.init()


def run_interface() -> None:
    """Runs the menu that allows the user to adjust the simulation conditions.
    """
    pygame.display.set_caption('Simulation Conditions')
    window_surface = pygame.display.set_mode((355, 365))

    background = pygame.Surface((355, 365))
    background.fill(pygame.Color('#FFFFFF'))

    manager = pygame_gui.UIManager((355, 365))

    create_category_boxes(manager)
    people_change, closeness_change, infected_change, connected_change = create_value_boxes(manager)

    num_people_plus, closeness_plus, infected_plus, connected_plus = plus_buttons(manager)
    num_people_minus, closeness_minus, infected_minus, connected_minus = minus_buttons(manager)

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

                    elif event.ui_element == num_people_minus and variable_values[0] > 10 and \
                            variable_values[0] > int(math.ceil(variable_values[2] / 10) * 10):
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

                    # Generate Button and start simulation
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


def create_category_boxes(manager: pygame_gui.UIManager) -> None:
    """Creates four text boxes representing the different variables that can be adjusted: number of
    people, level of closeness, starting number of infected, and whether or not the graph is
    connected.
    """
    pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((25, 25), (200, 55)),
                                  html_text='Number of People: ', manager=manager)

    pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((25, 85), (200, 55)),
                                  html_text='Level of Closeness: ', manager=manager)

    pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((25, 145), (200, 55)),
                                  html_text='Starting Number of Infected: ', manager=manager)

    pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((25, 205), (200, 55)),
                                  html_text='Connected: ', manager=manager)


def create_value_boxes(manager: pygame_gui.UIManager) -> Tuple[pygame_gui.elements.UITextBox,
                                                               pygame_gui.elements.UITextBox,
                                                               pygame_gui.elements.UITextBox,
                                                               pygame_gui.elements.UITextBox]:
    """Creates four text boxes representing values of the four categories of the simulation."""
    people_change = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((200, 25), (75, 55)),
                                                  html_text='20', manager=manager)

    closeness_change = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((200, 85), (75, 55)),
                                                     html_text='medium', manager=manager)

    infected_change = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((200, 145), (75, 55)),
                                                    html_text='1', manager=manager)

    connected_change = pygame_gui.elements.UITextBox(
        relative_rect=pygame.Rect((200, 205), (75, 55)),
        html_text='yes', manager=manager)

    return (people_change, closeness_change, infected_change, connected_change)


def plus_buttons(manager: pygame_gui.UIManager) -> Tuple[pygame_gui.elements.UIButton,
                                                         pygame_gui.elements.UIButton,
                                                         pygame_gui.elements.UIButton,
                                                         pygame_gui.elements.UIButton]:
    """Creates plus buttons that allow the user to increase the variables of the simulation."""
    num_people_plus = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((280, 25), (50, 25)),
                                                   text='+', manager=manager)
    closeness_plus = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((280, 85), (50, 25)),
                                                  text='+', manager=manager)
    infected_plus = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((280, 145), (50, 25)),
                                                 text='+', manager=manager)
    connected_plus = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((280, 205), (50, 25)),
                                                  text='+', manager=manager)

    return (num_people_plus, closeness_plus, infected_plus, connected_plus)


def minus_buttons(manager: pygame_gui.UIManager) -> Tuple[pygame_gui.elements.UIButton,
                                                          pygame_gui.elements.UIButton,
                                                          pygame_gui.elements.UIButton,
                                                          pygame_gui.elements.UIButton]:
    """Creates minus buttons that allow the user to decrease the variables of the simulation."""
    num_people_minus = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((280, 55), (50, 25)),
                                                    text='-', manager=manager)

    closeness_minus = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((280, 115), (50, 25)),
                                                   text='-', manager=manager)

    infected_minus = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((280, 175), (50, 25)),
                                                  text='-', manager=manager)

    connected_minus = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((280, 235), (50, 25)),
                                                   text='-', manager=manager)

    return (num_people_minus, closeness_minus, infected_minus, connected_minus)


def change_interval(variable_values: List[float], textbox, delta: float, dataset: int) -> None:
    """Changes the value of the variable for the selected dataset by a given delta"""
    variable_values[dataset] += delta
    if dataset == 1 or dataset == 3:
        textbox.html_text = determine_step(dataset, int(variable_values[dataset]))

    else:
        value = str(variable_values[dataset])
        textbox.html_text = value

    textbox.rebuild()


def determine_step(dataset: int, variable_value: int) -> str:
    """Determine which step to display on the menu based on the given dataset.

    Preconditions:
        - dataset == 1 or dataset == 3

    >>> determine_step(1, 0)
    'low'
    >>> determine_step(3, 0)
    'no'
    """
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
