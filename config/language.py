import gettext
import locale
import os

def set_language(lang):
    localedir = os.path.join(os.path.dirname(__file__), '../locale')
    lang_trans = gettext.translation(
        'messages',
        localedir=localedir,
        languages=[lang],
        fallback=True
    )
    # 显式安装到当前模块的全局命名空间
    lang_trans.install(names=('gettext', 'ngettext'))

    # 更新全局 _ 引用（确保 IDE 识别）
    global _
    _ = lang_trans.gettext
    return _

if __name__ =='__main__':
    # 设置为中文
    set_language('zh_CN')
    print(_("Hello, World!"))  # 输出：你好，世界！