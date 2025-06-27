# ui.py
import pygame
from settings import * # Import necessary settings

# --- Button Class (Using Images) ---
class Button:
    def __init__(self, center_x, center_y, text, text_color, font, image_normal, image_hover=None):
        """
        Initializes a button using images.
        Args:
            center_x (int): Center x-coordinate for the button.
            center_y (int): Center y-coordinate for the button.
            text (str): Text to display on the button.
            text_color (tuple): RGB color for the text.
            font (pygame.font.Font): Font object for the text.
            image_normal (pygame.Surface): Surface for the button's normal state.
            image_hover (pygame.Surface, optional): Surface for hover state. Defaults to None (uses normal image).
        """
        self.image_normal = image_normal
        # Use normal image for hover if hover image isn't provided or failed to load
        self.image_hover = image_hover if image_hover else image_normal

        self.image = self.image_normal # Current image to display
        self.rect = self.image.get_rect(center=(center_x, center_y))

        self.text = text
        self.text_color = text_color
        self.font = font
        self.is_hovered = False

        # Render text once (can be done if text/font doesn't change)
        # Or render in draw() if text needs to change dynamically
        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, screen):
        # Choose image based on hover state
        current_image = self.image_hover if self.is_hovered else self.image_normal
        # Blit the button image
        screen.blit(current_image, self.rect.topleft)
        # Blit the text centered on the button image's rect
        # Recalculate text rect center in case button image/rect changes (it shouldn't here, but safer)
        self.text_rect.center = self.rect.center
        screen.blit(self.text_surf, self.text_rect)

    def check_hover(self, mouse_pos):
        # Update hover state based on collision with the button's rect
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        # No need to return hover state unless used elsewhere

    def is_clicked(self, event):
        # Check for left mouse button down while hovered
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered

# --- Text Drawing Helper (Unchanged) ---
def draw_text(text, font, color, surface, x, y, center=False):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    if center: textrect.center = (x, y)
    else: textrect.topleft = (x, y)
    surface.blit(textobj, textrect)