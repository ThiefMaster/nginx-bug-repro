from urllib.parse import quote
from flask import Flask, url_for, request


app = Flask(__name__)


@app.route('/')
def index():
    return f'''
        WITHOUT explicitly encoding x-accel-redirect url:<br>
        <a href="{url_for('test_without')}">Test [main url without encoding, target without encoding]</a><br>
        <a href="{url_for('test_without', enc_target=1)}">Test [main url without encoding, target with encoding]</a> 💣<br>
        <br>
        <a href="{url_for('test_with')}">Test [main url with encoding, target without encoding]</a><br>
        <a href="{url_for('test_with', enc_target=1)}">Test [main url with encoding, target with encoding]</a><br>
        <br><br>
        WITH explicitly encoding x-accel-redirect url:<br>
        <a href="{url_for('test_without', enc_xar=1)}">Test [main url without encoding, target without encoding]</a><br>
        <a href="{url_for('test_without', enc_xar=1, enc_target=1)}">Test [main url without encoding, target with encoding]</a><br>
        <br>
        <a href="{url_for('test_with', enc_xar=1)}">Test [main url with encoding, target without encoding]</a><br>
        <a href="{url_for('test_with', enc_xar=1, enc_target=1)}">Test [main url with encoding, target with encoding]</a> ⚠
    '''


def _test():
    endpoint = 'target_with' if request.args.get('enc_target') == '1' else 'target_without'
    path = url_for(endpoint)
    internal_url = f'/_internal/http/{request.host}{path}'
    print(f'Redirecting internally to {internal_url}')
    response = app.make_response('')
    if request.args.get('enc_xar') == '1':
        internal_url = quote(internal_url)
    response.headers['X-Accel-Redirect'] = internal_url
    return response


@app.route('/test-without/')
def test_without():
    return _test()


@app.route('/test with/')
def test_with():
    return _test()


def _target():
    return f"target called url={request.base_url}"


@app.route('/target-without')
def target_without():
    return _target()


@app.route('/target with')
def target_with():
    return _target()


@app.errorhandler(404)
def notfound(exc):
    return f'NOT FOUND: {request.base_url}'
