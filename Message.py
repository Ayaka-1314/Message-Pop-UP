import os
import sys
import json
import tkinter as tk
from PIL import ImageTk, Image
from datetime import datetime
import traceback

class MessagePopup:
    THEMES = {
        'Light': {
            'bg': '#FFFFFF',
            'fg_title': '#333333',
            'fg_msg': '#666666',
            'fg_time': '#999999'
        },
        'Dark': {
            'bg': '#222222',
            'fg_title': '#EEEEEE',
            'fg_msg': '#CCCCCC',
            'fg_time': '#AAAAAA'
        },
        'Black_gold': {
            'bg': '#1A1A1A',
            'fg_title': '#FFD700',
            'fg_msg': '#CCCCCC',
            'fg_time': '#AAAAAA'
        }
    }

    def __init__(self):
        # 获取程序所在目录
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.message_count = 0
        self.active_popups = []
        self.root = tk.Tk()
        self.root.withdraw()
        self.max_messages = 5
        self.current_theme = self.load_theme()
        self.app_icons = {}  # 缓存应用图标
        
        # 预加载主题图标
        self.load_theme_icons()
        
        sys.excepthook = self.handle_exception
        self.setup_command_handler()

    def load_theme(self):
        """从配置文件加载主题设置"""
        try:
            settings_path = os.path.join(self.base_dir, 'settings.json')
            if os.path.exists(settings_path):
                with open(settings_path, 'r') as f:
                    settings = json.load(f)
                    return settings.get('theme', 'Light')
        except Exception as e:
            print(f"加载主题设置失败: {e}")
        return 'Light'

    def save_theme(self, theme):
        """保存主题设置到文件"""
        try:
            settings = {'theme': theme}
            settings_path = os.path.join(self.base_dir, 'settings.json')
            with open(settings_path, 'w') as f:
                json.dump(settings, f)
        except Exception as e:
            print(f"保存主题设置失败: {e}")

    def load_theme_icons(self):
        """预加载当前主题的所有应用图标"""
        theme_dir = os.path.join(self.base_dir, self.current_theme)
        print(f"[DEBUG] 正在从目录加载图标: {theme_dir}")
        
        if not os.path.exists(theme_dir):
            print(f"[WARNING] 主题目录不存在: {theme_dir}")
            os.makedirs(theme_dir, exist_ok=True)
            
        for app in ['message', 'wechat', 'qq']:
            icon_name = f"{app}-{self.current_theme}.png"
            icon_path = os.path.join(theme_dir, icon_name)
            
            # 如果图标不存在，创建默认图标并保存
            if not os.path.exists(icon_path):
                print(f"[WARNING] 图标不存在，创建默认图标: {icon_path}")
                default_img = self.create_default_icon(app)
                try:
                    default_img._PhotoImage__photo.write(icon_path, format='png')
                except:
                    pass
            
            try:
                img = Image.open(icon_path).resize((40, 40))
                self.app_icons[app] = ImageTk.PhotoImage(img)
                print(f"[DEBUG] 成功加载图标: {icon_name}")
            except Exception as e:
                print(f"[ERROR] 加载图标失败: {e}")
                self.app_icons[app] = self.create_default_icon(app)

    def create_default_icon(self, app_type):
        """创建默认图标"""
        colors = {
            'message': '#4CAF50',  # 绿色
            'wechat': '#07C160',   # 微信绿
            'qq': '#12B7F5'        # QQ蓝
        }
        color = colors.get(app_type, '#4CAF50')
        
        # 创建一个简单的带文字的默认图标
        img = Image.new('RGB', (40, 40), color=color)
        return ImageTk.PhotoImage(img)

    def get_app_icon(self, app_type):
        """获取应用图标"""
        return self.app_icons.get(app_type, self.create_default_icon('message'))

    def handle_exception(self, exc_type, exc_value, exc_traceback):
        with open("error.log", "a") as f:
            traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)
        self.root.quit()

    def create_popup(self, app_type='message'):
        popup = tk.Toplevel(self.root)
        popup.overrideredirect(True)
        popup.attributes('-alpha', 0)
        popup.attributes('-topmost', True)
        popup.attributes('-transparentcolor', '#f0f0f0')
        popup.geometry("320x80+1000+100")

        theme = self.THEMES[self.current_theme]
        frame = tk.Frame(popup, bg=theme['bg'], bd=0, highlightthickness=0)
        frame.place(x=0, y=0, width=320, height=80)

        # 应用图标
        icon_img = self.get_app_icon(app_type)
        icon_label = tk.Label(frame, image=icon_img, bg=theme['bg'])
        icon_label.image = icon_img
        icon_label.place(x=15, y=20)

        # 应用标题
        app_name = {
            'message': '系统消息',
            'wechat': '微信',
            'qq': 'QQ'
        }.get(app_type, 'APP')

        title_label = tk.Label(frame, text=app_name, bg=theme['bg'], 
                             fg=theme['fg_title'], font=('Microsoft YaHei', 12, 'bold'), 
                             anchor='w')
        title_label.place(x=70, y=15)

        # 消息内容
        msg_text = {
            'message': f"新的消息 *{self.message_count}",
            'wechat': "收到新的微信消息",
            'qq': "收到新的QQ消息"
        }.get(app_type, f"新的消息 *{self.message_count}")

        msg_label = tk.Label(frame, text=msg_text, bg=theme['bg'], 
                           fg=theme['fg_msg'], font=('Microsoft YaHei', 10))
        msg_label.place(x=70, y=40)

        # 时间
        time_str = datetime.now().strftime("%H:%M")
        time_label = tk.Label(frame, text=time_str, bg=theme['bg'], 
                            fg=theme['fg_time'], font=('Microsoft YaHei', 8))
        time_label.place(x=250, y=15)

        # 添加细边框增强视觉效果
        border_frame = tk.Frame(popup, bg='#DDDDDD', bd=0)
        border_frame.place(x=0, y=0, width=320, height=80, relwidth=1, relheight=1)
        frame.lift()

        return popup, frame

    def show_animation(self, popup, index):
        screen_width = self.root.winfo_screenwidth()
        target_x = screen_width - 340
        base_y = 20
        spacing = 85

        popup.geometry(f"320x80+{screen_width}+{base_y + index * spacing}")
        popup.deiconify()

        start_time = datetime.now().timestamp()
        duration = 250  # 动画持续时间(毫秒)

        def animate():
            elapsed = (datetime.now().timestamp() - start_time) * 1000
            progress = min(elapsed / duration, 1.0)
            
            # 平滑移动动画
            current_x = int(screen_width - (screen_width - target_x) * progress)
            popup.geometry(f"320x80+{current_x}+{base_y + index * spacing}")
            popup.attributes('-alpha', progress)

            # 挤压下方消息效果
            if index > 0:
                for i in range(index):
                    offset = int(5 * (1 - progress))
                    if i < len(self.active_popups):
                        self.active_popups[i][0].geometry(
                            f"320x80+{target_x}+{base_y + i * spacing + offset}"
                        )

            if progress < 1.0:
                popup.after(16, animate)
            else:
                # 5秒后开始隐藏动画
                popup.after(5000, lambda: self.hide_animation(popup, index))

        animate()

    def hide_animation(self, popup, index):
        screen_width = self.root.winfo_screenwidth()
        base_y = 20
        spacing = 85
        start_x = screen_width - 340

        start_time = datetime.now().timestamp()
        duration = 250  # 动画持续时间(毫秒)

        def animate():
            elapsed = (datetime.now().timestamp() - start_time) * 1000
            progress = min(elapsed / duration, 1.0)
            
            # 向右滑出动画
            current_x = int(start_x + 320 * progress)
            popup.geometry(f"320x80+{current_x}+{base_y + index * spacing}")
            popup.attributes('-alpha', 1 - progress)

            # 下方消息上移效果
            if index < len(self.active_popups) - 1:
                for i in range(index + 1, len(self.active_popups)):
                    offset = int(5 * progress)
                    if i < len(self.active_popups):
                        self.active_popups[i][0].geometry(
                            f"320x80+{screen_width - 340}+{base_y + i * spacing - offset}"
                        )

            if progress < 1.0:
                popup.after(16, animate)
            else:
                popup.destroy()
                self.reposition_after_hide(index)

        animate()

    def reposition_after_hide(self, removed_index):
        """消息消失后重新排列剩余消息"""
        screen_width = self.root.winfo_screenwidth()
        base_y = 20
        spacing = 85
        
        # 过滤掉已销毁的弹窗
        self.active_popups = [p for p in self.active_popups if p[0].winfo_exists()]
        
        # 重新定位所有消息
        for i, (popup, _) in enumerate(self.active_popups):
            target_y = base_y + i * spacing
            popup.geometry(f"320x80+{screen_width - 340}+{target_y}")

    def show_message(self, app_type='message'):
        self.message_count += 1
        
        # 移除最旧的消息如果达到上限
        if len(self.active_popups) >= self.max_messages:
            oldest_popup = self.active_popups.pop()
            oldest_popup[0].destroy()

        # 创建新弹窗
        popup, frame = self.create_popup(app_type)
        self.active_popups.insert(0, (popup, frame))
        
        # 显示动画
        self.show_animation(popup, 0)

    def change_theme(self, theme):
        """切换主题"""
        if theme in self.THEMES:
            self.current_theme = theme
            self.save_theme(theme)
            self.load_theme_icons()  # 重新加载图标
            print(f"主题已切换为: {theme}")
            
            # 更新所有现有弹窗的样式
            for popup, frame in self.active_popups:
                if popup.winfo_exists():
                    popup.destroy()
            self.active_popups = []
        else:
            print("无效的主题名称")

    def setup_command_handler(self):
        def check_command():
            cmd = input("输入命令 (text message/wechat/qq, theme Light/Dark/Black_gold, exit): ").strip()
            
            if cmd.startswith('text '):
                app_type = cmd[5:].lower()
                if app_type in ['message', 'wechat', 'qq']:
                    self.root.after(0, lambda: self.show_message(app_type))
                else:
                    print("无效的应用类型，请输入: text message/wechat/qq")
            elif cmd.startswith('theme '):
                theme = cmd[6:].strip().capitalize()
                self.change_theme(theme)
            elif cmd.lower() == 'exit':
                self.root.quit()
                return
            else:
                print("无效的命令，请输入:")
                print("  text message/wechat/qq - 显示消息")
                print("  theme Light/Dark/Black_gold - 切换主题")
                print("  exit - 退出程序")
                
            self.root.after(100, check_command)
        
        self.root.after(100, check_command)

    def run(self):
        print("消息弹窗系统已启动...")
        print(f"当前主题: {self.current_theme}")
        print("可用命令:")
        print("  text message/wechat/qq - 显示对应应用的消息")
        print("  theme Light/Dark/Black_gold - 切换主题")
        print("  exit - 退出程序")
        self.root.mainloop()

if __name__ == "__main__":
    app = MessagePopup()
    app.run()