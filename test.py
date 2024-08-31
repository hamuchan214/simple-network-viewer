import asyncio
from pysnmp.hlapi.v3arch.asyncio import *

async def get_cpu_utilisation():
    snmpEngine = SnmpEngine()

    iterator = getCmd(
        snmpEngine,
        CommunityData('viewers', mpModel=1),  # SNMPv2c でのコミュニティ文字列
        UdpTransportTarget(('192.168.10.11', 161)),  # スイッチのIPアドレスとポート
        ContextData(),
        ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0'))  # 取得するOID
    )

    errorIndication, errorStatus, errorIndex, varBinds = await iterator

    if errorIndication:
        print(f"Error: {errorIndication}")
    elif errorStatus:
        print(f"Error: {errorStatus.prettyPrint()} at {errorIndex} varBind {varBinds[int(errorIndex)-1]}")
    else:
        for varBind in varBinds:
            print(f"{varBind[0].prettyPrint()} = {varBind[1].prettyPrint()}")

    snmpEngine.closeDispatcher()

# メインのイベントループで非同期関数を実行
asyncio.run(get_cpu_utilisation())
