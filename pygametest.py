import pygame
from schedule_rect import ScheduleRect

pygame.display.init()
pygame.font.init()

# Set screen width and height here
screen_width = 1200
screen_height = 800
# Initialize the screen
screen = pygame.display.set_mode((screen_width, screen_height))
# name the screen
pygame.display.set_caption("Optimal Timetable Builder")
screen.fill((255, 255, 255))  # Fill screen with white

# This is just a test display
sched_test = ScheduleRect(100, 100, 200, 100, [])

base_schedule = []
# Main table creation
days = ["TIME", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"]
for i in range(0, 6):
    for c in range(0, 14):
        if c == 0:
            base_schedule.append(ScheduleRect(i * 167 + 183, 50 * c + 75, 167, 50, [days[i]]))
        elif i == 0:
            time_text = str(c + 8) + ":00" + "-" + str(c + 9) + ":00"
            base_schedule.append(ScheduleRect(i * 167 + 183, 50 * c + 75, 167, 50, [time_text]))
        else:
            base_schedule.append(ScheduleRect(i * 167 + 183, 50 * c + 75, 167, 50, []))

show_timetable = True
while show_timetable:
    pygame.display.update()

    for sched_rect in base_schedule:
        sched_rect.display(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
