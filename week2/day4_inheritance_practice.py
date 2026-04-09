class Vehicle:
    def __init__(self, brand):
        self.brand = brand

    def move(self):
        return f"{self.brand} 正在移动"


class Car(Vehicle):
    def __init__(self, brand, fuel_type):
        super().__init__(brand)
        self.fuel_type = fuel_type

    def move(self):
        return f"{self.brand} 汽车（{self.fuel_type}）正在行驶"

    def honk(self):
        return "嘀嘀！"


class Bicycle(Vehicle):
    def __init__(self, brand, gear_count):
        super().__init__(brand)
        self.gear_count = gear_count

    def move(self):
        return f"{self.brand} 自行车（{self.gear_count}速）正在骑行"


def test_car():
    # 创建Car实例
    my_car = Car("小米su7", "纯电")

    # 测试所有方法
    print("=== Car测试 ===")
    print(f"品牌: {my_car.brand}")
    print(f"燃料类型: {my_car.fuel_type}")
    print(f"移动: {my_car.move()}")  # 输出：小米su7 汽车（纯电）正在行驶
    print(f"鸣笛: {my_car.honk()}")   # 输出：嘀嘀！


def test_bicycle():
    # 创建Bicycle实例
    my_bicycle = Bicycle("光明", 20)

    # 测试所有方法
    print("\n=== Bicycle测试 ===")
    print(f"品牌: {my_bicycle.brand}")
    print(f"档位数: {my_bicycle.gear_count}速")
    print(f"移动: {my_bicycle.move()}")  # 输出：光明 自行车（20速）正在骑行


if __name__ == "__main__":
    test_car()
    test_bicycle()
