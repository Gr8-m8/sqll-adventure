"""console ANSI"""
class textdecoration:
    """Common text ANSI codes"""
    BGWHITE = '\033[107m'
    BGCYAN = '\033[106m'
    BGPURPLE = '\033[105m'
    BGBLUE = '\033[104m'
    BGYELLOW = '\033[103m'
    BGGREEN = '\033[102m'
    BGRED = '\033[101m'
    BGGRAY = '\033[100m'
    BGBLACK = '\033[40m'
    
    CYAN = '\033[96m'
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    GRAY = '\033[90m'

    STRIKETHROUGH = '\033[28m'
    UNDERLINE = '\033[4m'
    ITALICS = '\033[3m'
    BOLD = '\033[1m'
    END = '\033[0m'

    @classmethod
    def bg_list(cls):
        """List BG ANSI"""
        return [cls.BGWHITE, cls.BGBLACK, cls.BGBLUE, cls.BGCYAN, cls.BGGRAY, cls.BGGREEN, cls.BGRED, cls.BGPURPLE, cls.BGYELLOW]
    
