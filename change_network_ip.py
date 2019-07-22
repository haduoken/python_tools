import os

target_ip = '172.20.34.4'
target_gateway = '172.20.34.1'
target_netmask = '255.255.255.0'

# 得到ifconfig的 网卡名与ip
p = os.popen('ifconfig')
content = p.read()
content=content.split('\n')

contain_net_name =[]
for cur,l in enumerate(content):
    if 'Link encap:' in l:
        contain_net_name.append((cur,l))
net_name = []
for l in contain_net_name:
    l = l[1].split(' ')
    net_name.append(l[0])
print('net_name {}'.format(net_name))

# 具有 'inet addr:' 同时在net_name的下一行
contain_net_addr = []
for cur,l in enumerate(content):
    if 'inet addr:' in l:
        contain_net_addr.append((cur, l))
net_addr = []
for l in contain_net_addr:
    l = l[1].split(' ')
    for content in l:
        if 'addr:' in content:
            content = content[content.find(':')+1:]
            # l = l[1].split(':')[1]
            net_addr.append(content)
print('net_addr {}'.format(net_addr))

# 得到172开始的对应网络名
target_net_name = None
for name,addr in zip(net_name,net_addr):
    if '172.16.2.' in addr:
        target_net_name = name
        print('net name is {}'.format(name))

write_lines = []
# write_lines.append(l)
write_lines.append('\n')
write_lines.append('# add by scripy')
write_lines.append('auto {} \n'.format(target_net_name))
write_lines.append('iface {} inet static \n'.format(target_net_name))
write_lines.append('address {} \n'.format(target_ip))
write_lines.append('gateway {} \n'.format(target_gateway))
write_lines.append('netmask {} \n'.format(target_netmask))
# 将list转成str
out_lines = ''.join(write_lines)
# os.system('sudo a')
cmd = " echo '{}' >> /etc/network/test".format(out_lines)
cmd = 'sudo sh -c "{}"'.format(cmd)
os.system(cmd)
