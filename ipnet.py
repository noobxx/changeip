# -*- coding: utf-8 -*-
#测试一个网段内哪些ip可以上网
import wmi
import time
import os
wmiService = wmi.WMI()
colNicConfigs = wmiService.Win32_NetworkAdapterConfiguration(IPEnabled=True)
if len(colNicConfigs) < 1:
    print'没有找到可用的网络适配器'
    exit()
objNicConfig = colNicConfigs[0]
def ping(i):
    arrIPAddresses = ['172.16.16.' + str(i+1)]
    arrSubnetMasks = ['255.255.255.0']
    arrDefaultGateways = ['172.16.16.1']
    arrGatewayCostMetrics = [1]
    arrDNSServers = ['8.8.8.8','114.114.114.114']
    intReboot = 0
    returnValue = objNicConfig.EnableStatic(IPAddress = arrIPAddresses, SubnetMask = arrSubnetMasks)
    if returnValue[0] == 0:
        print'设置IP成功'
    elif returnValue[0] == 1:
        print'设置IP成功'
        intReboot += 1
    else:
        print'修改IP失败: IP设置发生错误'
        exit()
    returnValue = objNicConfig.SetGateways(DefaultIPGateway= arrDefaultGateways,GatewayCostMetric= arrGatewayCostMetrics)
    if returnValue[0] == 0:
        print'设置网关成功'
    elif returnValue[0] == 1:
        print'设置网关成功'
        intReboot += 1
    else:
        print'修改IP失败: 网关设置发生错误'
        exit()
    returnValue = objNicConfig.SetDNSServerSearchOrder(DNSServerSearchOrder= arrDNSServers)
    if returnValue[0] == 0:
        print'设置DNS成功'
    elif returnValue[0] == 1:
        print'设置DNS成功'
        intReboot += 1
    else:
        print'修改IP失败: DNS设置发生错误'
        exit()

for i in range(255):
    ping(i)
    time.sleep(10)
    exit_code = os.system('ping www.baidu.com')

    if exit_code == 0:
        print 'ping ok'
        file = open('ipnet.txt', 'a')
        file.write('172.16.16.' + str(i + 1) + '\n')
        file.close()
    else:
        print 'ping fail'