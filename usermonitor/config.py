DATABASE_PATH = 'server/database/user-monitor.db'

# ssh loginIP allow/deny
HOSTS_ALLOW_PATH = '/etc/hosts.allow'
HOSTS_DENY_PATH = '/etc/hosts.deny'

# Month, English change to digit
MONTH_ENGLISH_TO_DIGIT = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05',\
                          'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}

# home dir, for command_operation_record
HOME_DIR = '/home'
GLOBAL_BASHRC_PATH = '/etc/bash.bashrc'

# ALIAS and UNALIAS
ALIAS_RM = "alias rm='rm -i'\n"
UNALIAS_RM = "unalias rm\n"
