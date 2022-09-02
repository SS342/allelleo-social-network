from pywebcopy import save_webpage
import validators

def webpage(url='https://social.webestica.com/', folder='C:\\Users\\alex2\\Desktop\\Networks\\0.1\App\\', name='test'):
    save_webpage(
        url=url,
        project_folder=folder,
        project_name=name,
        bypass_robots = True,
        debug = True,
        open_in_browser = True,
        delay=None,
        threaded=False
    )

webpage()
