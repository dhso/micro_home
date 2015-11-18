from flask_user import login_required, roles_required
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def run(db, app):
    @app.route('/qq_news/index')
    @login_required
    def _qq_news_index():
        return 'Hello World'