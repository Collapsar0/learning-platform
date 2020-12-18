from .base import client


def test_get(client):
    assert client.get('/project/1').status_code == 401
    assert client.post(
        '/session', json={
            'username': 'user1',
            'password': '123'
        }
    ).status_code == 201
    assert client.get('/project/1').json['name'] == 'project1'
    assert client.get('/project/2').json['name'] == 'project2'
    assert client.get('/project/3').status_code == 403
    assert client.get('/project/4').status_code == 404
    assert len(client.get('/project').json['projects']) == 2


def test_post(client):
    # 创建失败（未登录）
    assert client.post(
        '/project', json={
            'name': 'project',
            'tag': '123'
        }
    ).status_code == 401
    # 创建失败（重名）
    assert client.post(
        '/session', json={
            'username': 'user1',
            'password': '123'
        }
    ).status_code == 201
    assert client.post(
        '/project', json={
            'name': 'project1',
            'tag': '123'
        }
    ).status_code == 400
    # 创建成功
    assert client.post(
        '/project', json={
            'name': 'project',
            'tag': '123'
        }
    ).status_code == 201
    assert client.get('/project/4').json['name'] == 'project'


def test_put(client):
    # 修改失败（未登录）
    assert client.put(
        '/project/1', json={
            'name': 'project3',
            'tag': '123'
        }
    ).status_code == 401
    # 修改失败（项目不存在）
    assert client.post(
        '/session', json={
            'username': 'user1',
            'password': '123'
        }
    ).status_code == 201
    assert client.put(
        '/project/10', json={
            'name': 'project3',
            'tag': '123'
        }
    ).status_code == 404
    # 修改失败（项目不属于你）
    assert client.put(
        '/project/3', json={
            'name': 'project3',
            'tag': '123'
        }
    ).status_code == 403
    # 修改失败（项目重名）
    assert client.put(
        '/project/1', json={
            'name': 'project1',
            'tag': '123'
        }
    ).status_code == 400
    # 修改成功
    assert client.put(
        '/project/1', json={
            'name': 'project3',
            'tag': '123'
        }
    ).status_code == 200
    assert client.get('/project/1').json['name'] == 'project3'
