import os
from views import app

if __name__ == '__main__':
    try:
        with app.app_context():
            port = int(os.environ.get("PORT", 5000))
            app.run(host='0.0.0.0',port=app.config['PORT'],debug=True,use_reloader=True,threaded=True)
    except Exception as error:
        print('\n*** Exception ***\nerror: %s\n' %str(error))