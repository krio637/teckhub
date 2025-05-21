from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Creates a default avatar image'

    def handle(self, *args, **kwargs):
        # Create the profile_pics directory if it doesn't exist
        profile_pics_dir = os.path.join(settings.MEDIA_ROOT, 'profile_pics')
        os.makedirs(profile_pics_dir, exist_ok=True)

        # Set the size for the avatar
        size = (400, 400)
        
        # Create a new image with a purple background
        image = Image.new('RGB', size, color='#6f42c1')
        draw = ImageDraw.Draw(image)
        
        # Calculate coordinates for the main circle
        margin = 50
        circle_bbox = [margin, margin, size[0] - margin, size[1] - margin]
        
        # Draw the main white circle
        draw.ellipse(circle_bbox, fill='white')
        
        # Calculate coordinates for the head (smaller circle)
        head_margin = size[0] // 4
        head_bbox = [
            head_margin,
            head_margin,
            size[0] - head_margin,
            size[0] - head_margin
        ]
        
        # Draw the head
        draw.ellipse(head_bbox, fill='#6f42c1')
        
        # Calculate coordinates for the body (larger circle)
        body_margin_x = size[0] // 3
        body_margin_top = size[1] // 2
        body_margin_bottom = size[1] - margin
        body_bbox = [
            body_margin_x,
            body_margin_top,
            size[0] - body_margin_x,
            body_margin_bottom
        ]
        
        # Draw the body
        draw.ellipse(body_bbox, fill='#6f42c1')
        
        # Save the image
        output_path = os.path.join(profile_pics_dir, 'default.png')
        image.save(output_path, 'PNG')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created default avatar at {output_path}')
        ) 