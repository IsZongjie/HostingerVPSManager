import time
from hostinger_vps_manager.api import HostingerAPIClient
from hostinger_vps_manager.resources.account import AccountManager
from hostinger_vps_manager.resources.vps import VPSManager
from hostinger_vps_manager.resources.regions import RegionManager


def main():
    # 初始化客户端
    client = HostingerAPIClient()

    # 账户信息
    account = AccountManager(client)
    print(f"账户余额: ${account.get_balance():.2f}")

    # 区域列表
    regions = RegionManager(client)
    print("可用区域:", regions.list_regions())

    # 价格查询
    vps = VPSManager(client)
    print("\n可用套餐（美国区域）:")
    for plan in vps.get_prices(region="us"):
        print(f"{plan['name']}: ${plan['price']}/月")

    # 创建实例（实际购买会扣费，建议使用测试账户）
    # order_id = vps.create_instance(
    #     plan_id="kvm1",
    #     os="ubuntu_22_04",
    #     region="us"
    # )
    # print(f"\n订单已创建: {order_id}")

    # 操作现有实例（需要替换为实际实例ID）
    test_instance_id = "vps_12345"  # 替换为你的实例ID
    try:
        print(f"\n操作实例 {test_instance_id} 关机")
        vps.power_control(test_instance_id, "stop")

        # 等待操作完成
        time.sleep(10)

        instances = vps.list_instances()
        print("\n当前实例列表:")
        for instance in instances:
            print(f"{instance.id} ({instance.status}) - {instance.ip}")

        # 销毁实例（谨慎操作！）
        # vps.destroy_instance(test_instance_id)

    except Exception as e:
        print(f"\n操作失败: {str(e)}")


if __name__ == "__main__":
    main()