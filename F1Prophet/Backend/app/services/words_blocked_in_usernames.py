BLOCKED_USERNAMES = [
    'admin', 'administrator', 'root', 'superuser', 'moderator', 'mod',
    'staff', 'support', 'help', 'system', 'bot', 'automated',
    
    'f1prophet', 'f1-prophet', 'api', 'server', 'database', 'admin-panel',
    'dashboard', 'settings', 'profile-settings', 'account-settings',
    
    'api', 'webhook', 'callback', 'endpoint', 'service', 'app',
    
    'null', 'undefined', 'test', 'admin_test', 'root_access',
    'drop', 'delete', 'select', 'insert', 'update', 'exec',
    'script', 'eval', 'function', 'class', 'prototype',
    
    'user', 'guest', 'player', 'driver', 'team', 'race',
    'password', 'email', 'username', 'login', 'register',
    'default', 'example', 'test', 'demo', 'sample',
    'anonymous', 'unknown', 'noreply', 'noadmin',
    
    'abuse', 'spam', 'scam', 'hack', 'exploit', 'crack',
    'cheat', 'bot', 'fake', 'troll', 'hate', 'racist',
    
    'porn', 'xxx', 'sex', 'drug', 'cocaine', 'heroin',
    'kill', 'death', 'suicide', 'rape', 'hitler', 'nazi',
    'fuck',
    
    'official', 'verified', 'real', 'true', 'actual',
    'the_', 'official_', 'real_', 'true_',
    
    'config', 'settings', 'secret', 'key', 'token', 'auth',
    'cache', 'session', 'cookie', 'storage', 'database',
    
    '../', '..\\', 'etc/passwd', 'windows/system32',
    'c:\\', '/bin/', '/etc/', '/usr/',
]

def is_username_blocked(username):
    for blocked in BLOCKED_USERNAMES:
        if blocked.lower() in username.lower():
            return True
    return False