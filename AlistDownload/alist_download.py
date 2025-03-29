"""
任务名称
name: 通过Alist下载资源
定时规则
cron: 0,20,40,50 0,1,2,7,8,9,10,11,22 * * *
"""
from datetime import datetime
import requests
import os
# from config import ALIST_HOST, ALIST_USERNAME, ALIST_PASSWORD

def load_config():
    """加载配置信息"""
    config = None
    try:
        config = __import__("config")
    except ImportError:
        print("config.py 文件不存在，请检查配置！")
    return config

CONFIG = load_config()
if CONFIG is not None:
    HOST = CONFIG.ALIST_HOST
    USERNAME = CONFIG.ALIST_USERNAME
    PASSWORD = CONFIG.ALIST_PASSWORD
    ARIA2_URL = CONFIG.ARIA2_URL
    ARIA2_TOKEN = CONFIG.ARIA2_TOKEN
else:
    HOST = os.getenv('ALIST_HOST')
    USERNAME = os.getenv('ALIST_USERNAME')
    PASSWORD = os.getenv('ALIST_PASSWORD')
    ARIA2_URL = os.getenv('ARIA2_URL')
    ARIA2_TOKEN = os.getenv('ARIA2_TOKEN')
ALL_DOWNLOAD_FILES = {}
AUTHTOKEN_URL = f'{HOST}/api/auth/login/hash'
ALIST_FILELIST_URL = f'{HOST}/api/fs/list'
Authorization_ALIST = ""

def request(url, method='POST', data=None):
    """
    请求Alist
    @param url: 请求url
    @param method: 请求方法
    @param data: 请求数据
    @return: 请求结果
    """
    print(f'请求url: {url}')
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json;charset=UTF-8",
        "cookie": "version=2.3.2024102801; device_id=d6f78a67f6f39fb98d880bb42c2869e5; _l=zh; nas_id=Z0410102JDQN9; nas_name=Z4-DQN9; sign=061WjA0MTAxMDJKRFFOOV8xNzMwNzIwMzU2XzYxOTUyNjI0NjMwODcyNjI3OTAm4PRDDANoYrKBcew1m3CsGuKcvvQrxfrSH1eood4PL8MSCx9bRijkbLqUTaMPAZm3d7jSm3YWNLVPYuNgyxOK8aDi5WfJhm2r9owpm1Y5ryIoOm1tAxfxsxSChsICryeSHm3BgACHdm1kLPPZqTdQw4PACQm1yel1wRZwlSbHRYJBCRJJVPli9xETL5cUQToPvQtsFjEzIJU6dDAAFpOKXGPU8MMcPBVCYQVUdowIrnBXm1vZacItvRII9rAciZsi2m3M3TJsz375f5m1nm3IkGm1bDn1UbXoOT0Vd9UnV9YtxRxudHaUAgx0ZDm1m10GVw1uYm34QHNWY3GWy6cv2dJhUm2Mc6V7iQ8uvZllwm4m4; nasPubKey=-----BEGIN%20PUBLIC%20KEY-----%0AMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwMqY4ylSX9Uhwp0rlGH8%0ADaaLMd2raYRkoareaj/DsGO2BH/Y3roDaZCHwbxJMtb3sMfLx9HnHX6KQpyOgj9/%0AS4tNH6Y/JmxujS6F6lfx4lalShwJy0naqXJoJ17PigFQYkLgQcC7eLUObzVhtwgn%0AmnUrMXtdgDXVJkLzocxteCMfvpIEBuMZ/koaz5ZO/vDJVDIelAvO46QuD+8qpKjL%0AYeRSJtTNvJuLAjcB+ek5zxPDTXpufmK5r7v+3S2y5bpRVL+evTwsibvYEQd/QbxS%0A05eDIPf3832ewEbvINDqOFchSPtVh9umh4OzgD8MJOI2rlu7iYlUKUuZOPJyw7ju%0ABQIDAQAB%0A-----END%20PUBLIC%20KEY-----; token=103MV8xNzMwNzIwMzU2XzE2ODA2ODQ5NjhfZDZm1NzhhNjdm1Nm1YzOWZiOThkODgwYm1I0Mm1MyODY5ZTVfMTc2MTIxNTM0Mzdfcm18m4aR6A48LRTrj7n3am2nf9V2ESm26bdB7s5C7nnn4RSm2zGdeGC9fS0AlO4dkb3sHm3bEOp9bVesm3gv8TaqshnU8Um3fO00JUAFOwsYMzLRgurpym31IdSYLssdCBTzY4Km3HBYoBAPdRyWDLFiWL036TOpZfjxXsNjICGSUgdECIxC98YQo8m3EZq9csacTNCznsQAz24m2yund76WvvPRpD1DdHO6VbZS8flC5Vt5CdZ8iSft6Eki6z4v2JL6K7n9qm18m2SqP5AKlUZm24u53nedPI1QWiyDiZrtD2P3P3DDTphOEHGm3bZeBtdAhqEnBZk2aiAMcam3pQ8AXc0XXtOJhxsJGnTtKGgm4m4; username=17612153437; qcname=; nickname=17612153437; userid=1; isMaster=1; isLocal=0; deviceColor=al_deep_gray; devicePdt=z4; deviceMode=z4; plat=web; app=file; clientPublicIp=139.227.141.161; publicSwitch=true; device=Mac%E7%94%B5%E8%84%91; dkAuth=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJhZG1pbiIsInJvbGUiOjEsImV4cCI6MTczMDkxMTEzNn0.A809aUlOjjF-qfOO98sXqNSGwAnMs4QJZPutU1LWB90; session=eyJsb2dpbiI6IjVhMjQxZjY3NmRmZWM1Y2Y1NDQwYTcyZGQ4OTcwMzFlIn0.Z-JGHA.oHxHMU09xSdSklHvZq-e6MhRhXg",
        "dnt": "1",
        "host": HOST.replace('http://', ''),
        "origin": HOST,
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
    }
    if Authorization_ALIST:
        headers['authorization'] = Authorization_ALIST
    response = requests.request(method, url, headers=headers, json=data)
    return response.json()


def get_auth_token():
    """
    获取auth_token
    @return: auth_token
    """
    print('获取auth_token')
    data = {
        "username": USERNAME,
        "password": PASSWORD,
        "otp_code": ""
    }
    response = request(AUTHTOKEN_URL, 'POST', data)
    code = response['code']
    if code is not None and code == 200:
        return response['data']['token']
    else:
        return None

def get_alist_file_list(path):
    """
    获取Alist文件列表
    @param path: 文件路径
    @return: 文件列表
    """
    data = {
        "path": path,
        "password":"",
        "page":1,
        "per_page":0,
        "refresh":False
    }
    response = request(ALIST_FILELIST_URL, 'POST', data)
    try:
        return response['data']['content']
    except:
        return None

def get_valid_file(episode, tv_name):
    """
    过滤有效文件
    1. 文件名包含“.mp4 .mkv .rmvb”
    2. created时间(2025-03-28T15:50:36.37Z)在 今日0点 之后
    3. is_dir 为 False
    4. 文件名在ALL_DOWNLOAD_FILES中不存在
    @param episode: 文件信息
    @param tv_name: 电视剧名称
    @return: 是否有效
    """
    if episode['is_dir'] == True:
        return False
    global ALL_DOWNLOAD_FILES
    if episode['name'] in ALL_DOWNLOAD_FILES.get(tv_name, []):
        print(f'{episode["name"]}已经下载过')
        return False
    flag = episode['name'].endswith('.mp4') or episode['name'].endswith('.mkv') or episode['name'].endswith('.rmvb')
    if flag == False:
        return False
    # 过滤今日0点之后的文件
    if episode['created'] < datetime.now().strftime('%Y-%m-%d 00:00:00'):
        return False
    return True

def download_file(file_url, dir, file_name):
    """
    下载文件
    @param file_url: 文件url
    @param dir: 文件夹名称
    @param file_name: 文件名称
    """
    print(f'⏬⏬⏬⏬⏬⏬下载文件:{dir}/{file_name}')
    headers = {"Content-Type": "application/json"}
    data = {
        "jsonrpc": "2.0",
        "id": "quark.download",
        "method": "aria2.addUri",
        "params": [
            "token:"+ARIA2_TOKEN,
            [ file_url ],
            {
                "dir": f"/downloads/{dir}",
                "out": file_name,
                "split": 1024,
                "max-connection-per-server": 1024,
            }
        ]
    }
    print(ARIA2_URL)
    print(data)
    response = requests.post(ARIA2_URL, headers=headers, json=data)
    print(response.text)

def list_all_has_download_files():
    """
    获取已经下载的文件
    @return: 已经下载的文件列表
    """
    global ALL_DOWNLOAD_FILES
    download_path = os.path.abspath('/ql/data/download')
    if os.path.exists(download_path):
        for tv_name in os.listdir(download_path):
            # 构建完整的路径
            tv_fold_path = os.path.join(download_path, tv_name)
        ALL_DOWNLOAD_FILES[tv_name] = []
        for file in os.listdir(tv_fold_path):
            ALL_DOWNLOAD_FILES[tv_name].append(file)
        print(f'获取已经下载的文件成功: {ALL_DOWNLOAD_FILES}')
    else:
        print(f'获取已经下载的文件失败: {download_path}')

def main():
    """
    主函数
    """
    # 获取已经下载的文件
    list_all_has_download_files()

    global Authorization_ALIST
    # 获取auth_token
    token = get_auth_token()
    if token is None:
        print('获取auth_token失败')
        return
    Authorization_ALIST = token
    print('获取auth_token成功')
    print(Authorization_ALIST)

    # 获取文件列表
    root_dir = ["/夸克/电视剧", "/夸克/动漫"]
    for dir in root_dir:
        file_list = get_alist_file_list(dir)
        if file_list is None:
            print(f'获取{dir}文件夹失败')
            continue
        else:
            print(f'获取{dir}文件夹成功')
            for file in file_list:
                download_file_list = []
                file_name = file['name']
                file_list = get_alist_file_list(dir + '/' + file_name)
                if file_list is None:
                    print(f'    获取{dir}/{file_name}文件夹--失败')
                    continue
                else:
                    print(f'    {dir}/{file_name}文件夹--成功')
                    for episode in file_list:
                        if episode['is_dir'] == False:
                            file_path = dir + '/' + file_name + '/' + episode['name']
                            # print(f'        {file_path} --成功')
                            # 过滤有效文件
                            if get_valid_file(episode, file['name']):
                                print(f'        过滤有效文件-{file_path}')
                                download_file_list.append({
                                    # /夸克/动漫/凡人修仙传/136.mp4?sign=qwbtHGzfYiaTNBeJsOQzNFMSSsaUqBICKyCC7Ob_FNk=:0
                                    'file_url': f"{HOST}{file_path}?sign={episode['sign']}", 
                                    'dir': file['name'],
                                    'file_name': episode['name']
                                })
                download_file_list.sort(key=lambda x: x['file_name'])
                if len(download_file_list) > 0:
                    download_file_list = download_file_list[:5]
                    print(f'⏬⏬⏬⏬开始提交下载{file_name}: {len(download_file_list)}个文件')
                    for download in download_file_list:
                        download_file(download['file_url'], download['dir'], download['file_name'])
                    print(f'⏬⏬⏬⏬⏬⏬下载完成')
                else:
                    print(f'🍵🍵🍵🍵🍵🍵{file_name}没有文件需要下载')


if __name__ == '__main__':
    main()


# alist 文件列表
# {
#   "name": "雁回时",
#   "size": 0,
#   "is_dir": true,
#   "modified": "2025-03-28T15:50:36.542Z",
#   "created": "2025-03-28T15:50:36.542Z",
#   "sign": "",
#   "thumb": "",
#   "type": 1,
#   "hashinfo": "null",
#   "hash_info": null
# }