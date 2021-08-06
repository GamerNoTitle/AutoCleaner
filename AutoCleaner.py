
import time
from threading import Timer
import mcdreforged.api.all as MCDR

PLUGIN_METADATA = {
    'id': 'auto_cleaner',
    'version': '2.0.0',
    'name': 'AutoCleaner',
    'author': ['GamerNoTitle', 'zyxgad'],
    'description': '这可能是最不简单的MCDR自动扫地姬',
    'dependencies': {
        'mcdreforged': '>=1.0.0'
    }
}

SERVER_OBJ = None
clean_timer = None

config = {
    'delay': 300,
    'enable': True
}
is_clean_now = False

information = '''
§6====== AutoCleaner ======
§6Author：§dGamerNoTitle, zyxgad
§6Version：§dBuild V2.0.0
§6当前开启状态：§b{enabled}
§6扫地频率：{delay}s/次
--------------------
§b§l命令帮助：
§b!!ac §6查看帮助信息
§b!!ac enable [true/false] §6查询/开启/关闭自动扫地
§b!!ac clean §615秒后进行扫地
§b!!ac abort §6中断扫地
§b!!ac set <time> §6更改扫地间隔
§6====== AutoCleaner ======'''

def send_message(source: MCDR.CommandSource, *args, sep=' ', prefix='§b[AutoCleaner]§6'):
    if source is not None:
        source.reply(MCDR.RTextList(prefix, args[0], *([MCDR.RTextList(sep, a) for a in args][1:])))

def broadcast_message(*args, sep=' ', prefix='§b[AutoCleaner]§6'):
    if SERVER_OBJ is not None:
        SERVER_OBJ.broadcast(MCDR.RTextList(prefix, args[0], *([MCDR.RTextList(sep, a) for a in args][1:])))

def log_info(*args, sep=' ', prefix='§b[AutoCleaner]§6'):
    if SERVER_OBJ is not None:
        SERVER_OBJ.logger.info(MCDR.RTextList(prefix, args[0], *([MCDR.RTextList(sep, a) for a in args][1:])))

def clean_time_call():
    global clean_timer
    clean_timer = None
    pre_clean()
    if config['enable']:
        flushTimer()

def flushTimer():
    global clean_timer, is_clean_now
    if clean_timer is not None:
        clean_timer.cancel()
        clean_timer = None
    if not is_clean_now and config['enable']:
        clean_timer = Timer(config['delay'], clean_time_call)
        clean_timer.start()

def command_help(source: MCDR.CommandSource):
    send_message(source, information.format(enabled=config['enable'], delay=config['delay']), prefix='')

def command_query_enable(source: MCDR.CommandSource):
    if config['enable']:
        send_message(source, '已开启自动扫地，自动清扫将每{}秒进行一次！'.format(config['delay']))
    else:
        send_message(source, '已关闭自动扫地')

def command_set_enable(source: MCDR.CommandSource, value: bool):
    config['enable'] = value
    if config['enable']:
        broadcast_message('玩家§d{}§6已开启自动扫地，自动清扫将每{}秒进行一次！'.format(source.player, config['delay']))
    else:
        broadcast_message('玩家§d{}§6已关闭自动扫地，自动清扫将不会运行！'.format(source.player))

@MCDR.new_thread('AC')
def command_clean(source: MCDR.CommandSource):
    global is_clean_now
    if is_clean_now or not config['enable']:
        return
    broadcast_message('玩家§d{}§6发起了扫地'.format(source.player))
    pre_clean()

def command_abort(source: MCDR.CommandSource):
    global is_clean_now
    if not is_clean_now or not config['enable']:
        return
    is_clean_now = False
    send_message(source, '中断扫地中')

def command_set_delay(source: MCDR.CommandSource, delay: int):
    config['delay'] = delay
    flushTimer()
    broadcast_message('玩家{}修改了扫地间隔, 服务器将每{}秒进行一次掉落物清理！'.format(source.player, config['delay']))

def pre_clean():
    global is_clean_now
    if is_clean_now or not config['enable']:
        return
    is_clean_now = True
    for i in range(15, 0, -1):
        broadcast_message('服务器将在{}秒后进行掉落物清扫，请注意捡回自己的物品！'.format(i))
        if not is_clean_now or not config['enable']:
            broadcast_message('已中断扫地')
            return
        time.sleep(1)
    if is_clean_now and config['enable']:
        clean_items()

def clean_items():
    global is_clean_now
    if not config['enable']:
        return
    SERVER_OBJ.execute('kill @e[type=item]')
    broadcast_message('扫地完成！下次扫地将在{}秒之后'.format(config['delay']))
    is_clean_now = False

def on_load(server, old_module):
    global SERVER_OBJ
    SERVER_OBJ = server
    server.register_command(
        MCDR.Literal('!!ac').
            runs(command_help).
            then(MCDR.Literal('enable').
                runs(command_query_enable).
                then(MCDR.Literal('true').runs(lambda src: command_set_enable(src, True))).
                then(MCDR.Literal('false').runs(lambda src: command_set_enable(src, False)))).
            then(MCDR.Literal('clean').runs(command_clean)).
            then(MCDR.Literal('abort').runs(command_abort)).
            then(MCDR.Literal('set').then(MCDR.Integer('t').requires(lambda src, ctx: ctx['t'] > 0, lambda: 'time 需要大于 0').
                runs(lambda src, ctx: command_set_delay(src, ctx['t'])))))
    broadcast_message('自动扫地已加载成功！服务器每{}秒将进行一次掉落物清理！'.format(config['delay']))

def on_unload(server: MCDR.ServerInterface):
    global SERVER_OBJ
    SERVER_OBJ = None
    global clean_timer
    if clean_timer is not None:
        clean_timer.cancel()
        clean_timer = None

def on_remove(server: MCDR.ServerInterface):
    global SERVER_OBJ
    SERVER_OBJ = None
    global clean_timer
    if clean_timer is not None:
        clean_timer.cancel()
        clean_timer = None
