from rich.console import Console
console = Console()

config = {

    'information': {
        'author': 'allelleo',
        'project_version': 0.4,
        'api_version': 1,
        "DataBase_version": 1.25,
        "Defense_version": 0.1,
        'Logs_version': 0.01,
    },
    'app': {
        'SECRET_KEY': "allelleo-secret-key",
        "JSON_AS_ASCII": False,
        "APPLICATION_ROOT": "/",
        "MAX_COOKIE_SIZE": 8192,
        "HOST": "localhost",
        "PORT": 5000,
    },
    'api': {
        'version': 1,
    },
    "DataBase": {
        'driver': 'sqlite3',
        'User': {
            'profile': {
                'all_sex': {
                    '0': 'Not stated',
                    '1': 'Male',
                    '2': 'Female',
                },
                'all_status': {
                    '0': 'Not stated',
                },
            },
            "users": {},
        },
    },
    "Defense": {},
    "Logs": {},
}

def LogConfig():
    console.log(f"Author: {config['information']['author']} ~ Project version: {config['information']['project_version']}")

LogConfig()
