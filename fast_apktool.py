import sys
import os
import logging
import zipfile
import shutil


def get_option_args(args):
    """
    获取命令行参数
    :param args:
    :return:
    """
    option_args = {}
    while args:
        if args[0][0] == '-':
            option_args[args[0]] = args[1]
            args = args[2:]
        else:
            args = args[1:]

    return option_args


def is_sourceapk_signed(src_path):
    """
    判断源APK是否已经被签名过
    :@param src_path
    :return:
    """
    src = zipfile.ZipFile(src_path)
    try:
        cert_sf = src.getinfo('META-INF/CERT.SF')
        cert_rsa = src.getinfo('META-INF/CERT.RSA')
    except Exception as e:
        print(e.__str__())
        return False
    else:
        if cert_sf or cert_rsa:
            return True
        else:
            return False


def write_apk_extra_info(src, rst, info_dict):
    """
    向apk写入信息
    :param src: 原路径
    :param rst: 生成目标目录
    :param info_dict: 信息字典
    :return:
    """
    rst = os.path.abspath(rst)+'/'
    for item in info_dict.items():
        rst += str(item[1]) + '_'
    rst = rst[:-1]+'.apk'

    if not os.path.exists(os.path.dirname(rst)):
        os.mkdir(os.path.dirname(rst))

    shutil.copy(src, rst)
    rst_zip = zipfile.ZipFile(rst, 'a', zipfile.ZIP_DEFLATED)
    tmp_file = os.path.dirname(os.path.abspath(__file__))+'/tmp'
    with open(tmp_file, 'w') as f:
        pass
    for item in info_dict.items():
        key = item[0][1:]
        value = item[1]
        zip_file_key = 'META-INF/{key}_{value}'.format(key=key, value=value)
        try:
            rst_zip.write(tmp_file, zip_file_key)
        except Exception as e:
            print(e.__str__())
    rst_zip.close()
    os.remove(tmp_file)
    return rst


def sign_handled_apk(ksconfig, unsigned_path):
    """
    签名apk
    :@param unsigned_path unsigned apk path
    :return:
    """
    signed_path = unsigned_path[:-4]+"_signed.apk"
    os.system("jarsigner -verbose -digestalg SHA1 -sigalg MD5withRSA -keystore " + ksconfig['keystore_path'] + " -storepass " + ksconfig['keystore_pwd'] + " -signedjar " + signed_path + " " + unsigned_path + " " + ksconfig['alias'] + " -keypass " + ksconfig['alias_pwd'])
    os.remove(unsigned_path)
    print("sing succes ", signed_path)
    pass

if __name__ == '__main__':
    args = get_option_args(sys.argv)
    if args.__len__() > 0:
        print('custom_params: ', args, sep='\n')
    else:
        result_dir = os.path.dirname(os.path.abspath(__file__)) + '/rst'
        source_dir = os.path.dirname(os.path.abspath(__file__)) + '/src/app.apk'
        args = {'-src': source_dir,
                '-rst': result_dir,
                '-ip': '192.168.1.10',
                '-port': 1851,
                '-channel': 'official'}
        print('default_params: ', args, sep='\n')

    source_dir = args.get('-src')
    if not source_dir:
        source_dir = os.path.dirname(os.path.abspath(__file__)) + '/src/app.apk'
    else:
        args.pop('-src')

    result_dir = args.get('-rst')
    if not result_dir:
        result_dir = os.path.dirname(os.path.abspath(__file__)) + '/rst'
    else:
        args.pop('-rst')

    # 初始化keysotre信息
    keystore_config = {}
    # keystore 路径
    keystore_path = args.get('-keystore')
    if not keystore_path:
        keystore_path = os.path.dirname(os.path.abspath(__file__)) + '/keystore/jdwb.jks'
    else:
        args.pop('-keystore')
    keystore_config['keystore_path'] = keystore_path
    # keystore password
    keystore_pwd = args.get('-keystorepwd')
    if not keystore_pwd:
        keystore_pwd = '123456'
    else:
        args.pop('-keystorepwd')
    keystore_config['keystore_pwd'] = keystore_pwd
    # keystore alias
    keystore_alias = args.get('-alias')
    if not keystore_alias:
        keystore_alias = 'jdwb'
    else:
        args.pop('-alias')
    keystore_config['alias'] = keystore_alias
    # keysotre alias password
    keystore_alias_pwd = args.get('-aliaspwd')
    if not keystore_alias_pwd:
        keystore_alias_pwd = '123456'
    else:
        args.pop('-aliaspwd')
    keystore_config['alias_pwd'] = keystore_alias_pwd

    if not os.path.exists(source_dir):
        '''
        源APK文件不存在
        '''
        logging.error(source_dir+' not exists!')
        exit('sorry goodbye!')

    if is_sourceapk_signed(source_dir):
        '''
        判断该包是否被签名过
        '''
        logging.error(source_dir+' has bean signed!')
    else:
        '''
        该包没有被签名过，开始打入用户自定义信息
        '''
        print(source_dir+" has't bean signed!")
        rst = write_apk_extra_info(source_dir, result_dir, args)
        sign_handled_apk(keystore_config, rst)
