import urequests as requests
import ujson as json
import uos as os


def get_app(host, version=None):

    if version is not None:
        url = '{}/api/v1/app/version?version={}'.format(host, version)
    else:
        url = '{}/api/v1/app/version'.format(host)

    result = requests.get(url)
    if result.status_code >= 400:
        return False

    try:
        data = result.json()

        set_next_version(data['version'])

        fpath = path_join('next', 'app.py')
        with open(fpath, 'w') as f:
            f.write(data['code'])

        # Sanity check
        from next.app import main
        return True
    except:
        pass

    return False


def path_join(*args):
    return '/'.join(args)


def makedirs(path, exists_ok=True):
    try:
        os.mkdir(path)
    except:
        if not exists_ok:
            raise


def rename_dir(old_dir, new_dir):
    # Allows to rename only one level of files
    makedirs(new_dir)
    for fname in os.listdir(old_dir):
        old_fpath = path_join(old_dir, fname)
        new_fpath = path_join(new_dir, fname)
        os.rename(old_fpath, new_fpath)

    os.rmdir(old_dir)


def read_json(path, default=None):
    try:
        with open(path) as f:
            data = json.load(f)

        return data
    except:
        print('Failed to read JSON: {}'.format(path))

    return default


def write_json(path, data):
    try:
        with open(path, 'w') as f:
            data = json.dump(data, f)
    except:
        print('Failed to write JSON: {}'.format(path))


CONFIG_FNAME = 'cfg.json'


def get_config():
    config = read_json(CONFIG_FNAME)
    return config


def set_config(config):
    write_json(CONFIG_FNAME, config)


INFO_FILE = 'info.json'


def get_current_version():
    fpath = path_join('last', INFO_FILE)
    data = read_json(fpath, {})
    return data.get('version')


def get_next_version():
    fpath = path_join('next', INFO_FILE)
    data = read_json(fpath, {})
    return data.get('version')


def set_next_version(version):
    makedirs('next')
    fpath = path_join('next', INFO_FILE)
    write_json(fpath, {'version': version})
