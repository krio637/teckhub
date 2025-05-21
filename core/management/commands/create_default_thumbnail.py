from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Creates a default course thumbnail image'

    def handle(self, *args, **kwargs):
        # Create the static/images directory if it doesn't exist
        static_dir = os.path.join(settings.BASE_DIR, 'static', 'images')
        os.makedirs(static_dir, exist_ok=True)

        # Set the size for the thumbnail
        size = (800, 400)
        
        # Create a new image with a gradient background
        image = Image.new('RGB', size)
        draw = ImageDraw.Draw(image)
        
        # Create a gradient background
        for y in range(size[1]):
            r = int(123 * (1 - y/size[1]))  # Gradient from purple to darker purple
            g = int(44 * (1 - y/size[1]))
            b = int(191 * (1 - y/size[1]))
            draw.line([(0, y), (size[0], y)], fill=(r, g, b))
        
        # Draw some decorative elements
        # Draw circles
        circle_positions = [
            (size[0]//4, size[1]//2, 100),
            (size[0]//2, size[1]//3, 80),
            (3*size[0]//4, size[1]//2, 120),
        ]
        
        for x, y, radius in circle_positions:
            draw.ellipse(
                [
                    (x - radius, y - radius),
                    (x + radius, y + radius)
                ],
                outline='white',
                width=3
            )
        
        # Add text placeholder shapes
        rect_positions = [
            (size[0]//2 - 150, size[1]//2 - 40, size[0]//2 + 150, size[1]//2 - 20),
            (size[0]//2 - 100, size[1]//2 + 10, size[0]//2 + 100, size[1]//2 + 30),
        ]
        
        for rect in rect_positions:
            draw.rectangle(rect, fill='white', width=2)
        
        # Save the image
        output_path = os.path.join(static_dir, 'default-thumbnail.jpg')
        image.save(output_path, 'JPEG', quality=95)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created default thumbnail at {output_path}')
        ) 