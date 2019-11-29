import os
import re
import subprocess
from datetime import datetime

# デモ用｡セキュリティ対策などはしていない｡
def main():
    sesstion_id = str(datetime.now().strftime('%s'))
    history_dir_path = 'history'
    if not os.path.exists(history_dir_path):
        os.mkdir(history_dir_path)

    gen_dir_path = history_dir_path + '/' + sesstion_id
    if not os.path.exists(gen_dir_path):
        os.mkdir(gen_dir_path)

    while True:
        try:
            packet_data = str(input('> packet_data :'))
            packet_data_length = int(input('> packet_data_length :'))
            break
        except ValueError:
            print('input is invalid.')
            continue

    packet_data_hex_list = []
    for i in range(0, len(packet_data)):
        hex_list = re.split('(..)', hex(ord(packet_data[i])).split('x')[-1])[1::2]
        for j in range(0, len(hex_list)):
            packet_data_hex_list.append('0x' + hex_list[j])

    # print(packet_data_hex_list)
    mb = '0x' + format(packet_data_length, '04x')[0:2]
    lb = '0x' + format(packet_data_length, '04x')[2:4]
    # print(mb, lb)

    packet_data_length_list = [mb, lb]

    packet_data_list = []
    packet_data_list.extend(packet_data_length_list)
    packet_data_list.extend(packet_data_hex_list)
    # print(packet_data_list)

    packet_data_list_str = ', '.join(packet_data_list)

    print('packet_data=[{}]'.format(packet_data_list_str))

    array_size_str = str(len(packet_data) + 2)

    # print(array_size_str)
    # print(packet_data_list_str)

    array_size_marker = 'XXXXX'
    array_elements_marker = 'YYYYY'
    print('###{}###'.format(sesstion_id))
    print('###c_heartbleed###')
    input('> (press enter)')
    c_heartbleed_path = 'c_heartbleed.c'
    with open(c_heartbleed_path) as f:
        c_heartbleed = f.read().replace(array_size_marker, array_size_str).replace(array_elements_marker, packet_data_list_str)

    gen_c_heartbleed_path_path = gen_dir_path + '/' + c_heartbleed_path
    with open(gen_c_heartbleed_path_path, mode='w') as f:
        f.write(c_heartbleed)

    exec_file_path = './' + gen_dir_path + '/c_heartbleed.out'
    command = ['gcc', gen_c_heartbleed_path_path, '-o', exec_file_path]
    print('###command###')
    print(' '.join(command))

    print('````c_heartbleed.c\n{}\n```\n'.format(c_heartbleed))
    print('###output###')
    try:
        res = subprocess.check_output(command, stderr=subprocess.STDOUT).decode('utf-8', 'ignore')
        print(res)
    except Exception as e:
        print(e.output.decode('utf-8', 'ignore'))

    command = [exec_file_path]
    print('###command###')
    print(' '.join(command))
    try:
        res = subprocess.check_output(command, stderr=subprocess.STDOUT).decode('utf-8', 'ignore')
        print(res)
    except Exception as e:
        print(e.output.decode('utf-8', 'ignore'))


    print('###rust_heartbleed###')
    input('> (press enter)')
    rust_heartbleed_path = 'rust_heartbleed.rs'
    with open(rust_heartbleed_path) as f:
        rust_heartbleed = f.read().replace(array_size_marker, array_size_str).replace(array_elements_marker, packet_data_list_str)
    gen_rust_heartbleed_path = gen_dir_path + '/' + rust_heartbleed_path
    with open(gen_rust_heartbleed_path, mode='w') as f:
        f.write(rust_heartbleed)
    # rustc rust_heartbleed.rs -o ./out/rust_heartbleed.out
    exec_file_path = './' + gen_dir_path + '/rust_heartbleed.out'
    command = ['rustc', gen_rust_heartbleed_path, '-o', exec_file_path]
    print('###command###')
    print(' '.join(command))
    print('````rust_heartbleed.rs\n{}\n```\n'.format(rust_heartbleed))
    print('###output###')
    try:
        res = subprocess.check_output(command, stderr=subprocess.STDOUT).decode('utf-8', 'ignore')
        print(res)
    except Exception as e:
        print(e.output.decode('utf-8', 'ignore'))

    command = [exec_file_path]
    print('###command###')
    print(' '.join(command))
    try:
        res = subprocess.check_output(command, stderr=subprocess.STDOUT).decode('utf-8', 'ignore')
        print(res)
    except Exception as e:
        print(e.output.decode('utf-8', 'ignore'))

    print('###fstar_heartbleed###')
    input('> (press enter)')
    fstar_heartbleed_path = 'fstar_heartbleed.c'
    with open(fstar_heartbleed_path) as f:
        fstar_heartbleed = f.read().replace(array_size_marker, array_size_str).replace(array_elements_marker, packet_data_list_str)

    gen_fstar_heartbleed_path = gen_dir_path + '/' + fstar_heartbleed_path
    with open(gen_fstar_heartbleed_path, mode='w') as f:
        f.write(fstar_heartbleed)

	# krml -verify -drop WasmSupport -drop C_Endianness -drop C -tmpdir ./out -fsopt --cache_dir -fsopt ./out -no-prefix Heartbleed -o ./out/fstar_heartbleed.out heartbleed.fst memcpy.c fstar_heartbleed.c

    exec_file_path = './' + gen_dir_path + '/fstar_heartbleed.out'
    command = ['krml', '-verify', '-drop', 'WasmSupport', '-drop', 'C_Endianness', '-drop', 'C', '-tmpdir', './' + gen_dir_path + '/out', '-fsopt', '--cache_dir', '-fsopt', './' + gen_dir_path + '/out', '-no-prefix', 'Heartbleed', '-o', exec_file_path, 'heartbleed.fst', 'memcpy.c', gen_fstar_heartbleed_path]
    print('###command###')
    print(' '.join(command))
    print('fstar_heartbleed.c````\n{}\n```\n'.format(fstar_heartbleed))
    print('###output###')
    try:
        res = subprocess.check_output(command, stderr=subprocess.STDOUT).decode('utf-8', 'ignore')
        print(res)
    except Exception as e:
        print(e.output.decode('utf-8', 'ignore'))

    command = [exec_file_path]
    print('###command###')
    print(' '.join(command))
    try:
        res = subprocess.check_output(command, stderr=subprocess.STDOUT).decode('utf-8', 'ignore')
        print(res)
    except Exception as e:
        print(e.output.decode('utf-8', 'ignore'))



if __name__ == '__main__':
    main()