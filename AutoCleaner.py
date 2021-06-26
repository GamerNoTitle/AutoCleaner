import time

delay=300
enabled = True

PLUGIN_METADATA = {
    'id': 'AutoCleaner',
    'version': '1.0.0',
    'name': '这可能是最简单的MCDR自动扫地姬'
}

def on_load(server,old_module):
    server.say('§b[AutoCleaner]§6自动扫地已加载成功！服务器每{}秒将进行一次掉落物清理！'.format(delay))
    while True:
        time.sleep(delay-15)
        if enabled:
            server.say('§b[AutoCleaner]§6还有§415§6秒后进行清理！请注意捡回自己的物品！')
        time.sleep(15)
        if enabled:
            server.execute('kill @e[type=item]')
            server.say('§b[AutoCleaner]§6扫地完成！')
    
def on_info(server,info):
    global enabled
    information = '''
    §6====== AutoCleaner ======
    §6Author：§dGamerNoTitle
    §6Version：§dBuild V1.0.0 for EMUnion
    §6当前开启状态：§b{}
    §6扫地频率：{}s/次
    --------------------
    §b§l命令帮助：
    §b!!ac §6查看帮助信息
    §b!!ac switch §6进行自动扫地开启切换
    §b!!ac clean §615秒后进行扫地
    '''.format(enabled,delay)
    if info.content == '!!ac':
        server.reply(info, information)
    if info.content == '!!ac switch':
        enabled = not(enabled)
        if enabled:
            server.say('§b[AutoCleaner]§6玩家§d{}§6已开启自动扫地，自动清扫将每{}秒进行一次！'.format(info.player,delay))
        else:
            server.say('§b[AutoCleaner]§6玩家§d{}§6已关闭自动扫地，自动清扫将不会运行！'.format(info.player))
    if info.content == '!!ac clean':
        server.say('§b[AutoCleaner]§6玩家§d{}§6发起了扫地，服务器将在15秒后进行掉落物清扫，请注意捡回自己的物品！'.format(info.player))
        time.sleep(15)
        server.execute('kill @e[type=item]')
        server.say('§b[AutoCleaner]§6扫地完成！')
