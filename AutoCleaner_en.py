import time

delay=300
enabled = True

PLUGIN_METADATA = {
    'id': 'AutoCleaner',
    'version': '1.0.0',
    'name': 'This may be the simplest auto cleaner of MCDR'
}

def on_load(server,old_module):
    server.say('§b[AutoCleaner]§6AutoCleaner loaded, The server will clean items every {} seconds!'.format(delay))
    while True:
        time.sleep(delay-15)
        if enabled:
            server.say('§b[AutoCleaner]§415§6 seconds to clean, please pick up your items that you don\'t want to lose!')
        time.sleep(15)
        if enabled:
            server.execute('kill @e[type=item]')
            server.say('§b[AutoCleaner]§6AutoCleaner process completed!')
    
def on_info(server,info):
    global enabled
    information = '''
    §6====== AutoCleaner ======
    §6Author: §dGamerNoTitle
    §6Version: §dBuild V1.0.0
    §6Enable: §b{}
    §6Frequency: §bevery {} seconds
    --------------------
    §b§lCommand help: 
    §b!!ac §6Checkout detailed information
    §b!!ac switch §6Enable/Disable auto clean process
    §b!!ac clean §6Clean for once after 15 seconds
    '''.format(enabled,delay)
    if info.content == '!!ac':
        server.reply(info, information)
    if info.content == '!!ac switch':
        enabled = not(enabled)
        if enabled:
            server.say('§b[AutoCleaner]§6AutoClean process has been enabled by §d{}§6. The server will clean items every {} seconds.'.format(info.player,delay))
        else:
            server.say('§b[AutoCleaner]§6AutoClean process has been disabled by §d{}§6. The server will not clean items automatically.'.format(info.player))
    if info.content == '!!ac clean':
        server.say('§b[AutoCleaner]§6A manual clean process has been submitted by §d{}§6. The server will clean items within 15 seconds.'.format(info.player))
        time.sleep(15)
        server.execute('kill @e[type=item]')
        server.say('§b[AutoCleaner]§6Clean process completed!')
