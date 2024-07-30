from PIL import Image

def crop_and_remove_background(input_path, output_path):
    # Mở hình ảnh
    with Image.open(input_path) as img:
        # Chuyển đổi sang chế độ RGBA để hỗ trợ trong suốt
        img = img.convert("RGBA")
        
        # Lấy kích thước ảnh
        width, height = img.size
        
        # Tìm ranh giới của nội dung không trong suốt
        left, top, right, bottom = width, height, 0, 0
        for x in range(width):
            for y in range(height):
                pixel = img.getpixel((x, y))
                if pixel[3] != 0:  # Nếu pixel không trong suốt
                    left = min(left, x)
                    top = min(top, y)
                    right = max(right, x)
                    bottom = max(bottom, y)
        
        # Cắt ảnh
        img = img.crop((left, top, right + 1, bottom + 1))
        
        # Tạo ảnh mới với nền trong suốt
        new_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
        
        # Dán ảnh đã cắt lên nền trong suốt
        new_img.paste(img, (0, 0), img)
        
        # Lưu ảnh mới
        new_img.save(output_path, "PNG")
    
    print(f"Đã lưu hình ảnh đã xử lý tại {output_path}")

# Sử dụng hàm
input_path = 'graphics/Player/Ninja/0.png'  # Thay đổi đường dẫn này
output_path = 'graphics/Player/Ninja/0_btn_no_bg.png'  # Thay đổi đường dẫn này
crop_and_remove_background(input_path, output_path)