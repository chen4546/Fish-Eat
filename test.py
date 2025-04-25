import pygame

# 初始化Pygame
pygame.init()

# 获取显示器的信息
info = pygame.display.Info()

# 打印分辨率
print(f"当前屏幕分辨率：{info.current_w}x{info.current_h}")

# 退出Pygame
pygame.quit()