鸣潮抽卡模拟器
一个基于《鸣潮》(Wuthering Waves) 游戏抽卡机制的Python模拟器，可以模拟游戏中的抽卡过程、保底机制和资源获取。

功能特性
🎯 精确概率模拟 - 严格按照游戏内的概率和保底机制实现

📊 详细统计功能 - 完整的抽卡记录和资源统计

🔄 灵活状态管理 - 轻松重置模拟器状态

🎪 自定义卡池 - 支持配置不同的限定角色和UP角色

📈 历史记录 - 保存每次抽卡的详细历史

🧮 资源计算 - 模拟辉光珊瑚和荡漾珊瑚的获取

安装要求
系统要求
Python 3.6 或更高版本

依赖库
bash
# 本项目仅使用Python标准库，无需额外安装依赖
# 主要使用的库：
# - random: 随机数生成
# - copy: 深拷贝功能
# - typing: 类型注解
快速开始
基本用法
python
from gacha_simulator import GachaSimulator

# 创建模拟器实例
simulator = GachaSimulator()

# 单次抽卡
item, afterglow_coral, oscillated_coral = simulator.pull()
print(f"获得: {item}")

# 多次抽卡模拟（显示每次结果）
result = simulator.simulate_pulls(10, show_details=True)

# 多次抽卡模拟（只显示摘要）
result = simulator.simulate_pulls(100, show_details=False)
print(f"总抽数: {result['total_pulls']}")
print(f"限定5星: {result['featured_5star_count']}")
完整示例
python
from gacha_simulator import GachaSimulator

# 初始化模拟器
simulator = GachaSimulator()

# 设置自定义卡池
simulator.set_banner(
    featured_5star="Jinhsi", 
    featured_4stars=["Sanhua", "Mortefi", "Yuanwu"]
)

# 模拟650抽（大保底期望）
result = simulator.simulate_pulls(650, show_details=False)

# 输出结果
print("=== 抽卡结果 ===")
print(f"总抽数: {result['total_pulls']}")
print(f"限定5星 {simulator.rate_up_5star}: {result['featured_5star_count']}")

if result['standard_5star_counts']:
    print("常驻5星:")
    for char, count in result['standard_5star_counts'].items():
        print(f"  {char}: {count}")

if result['star_4_counts']:
    print("4星角色:")
    for char, count in result['star_4_counts'].items():
        print(f"  {char}: {count}")

print(f"3星武器: {result['weapon_count']}")
print(f"辉光珊瑚: {result['total_afterglow_coral']}")
print(f"荡漾珊瑚: {result['total_oscillated_coral']}")
print(f"最终保底状态: {result['final_pity']}")
概率机制
5星角色概率
保底区间	概率	说明
1-65抽	0.8%	基础概率
66-70抽	0.8%-20.8%	线性增长
71-75抽	20.8%-60.8%	线性增长
76-78抽	60.8%-90.8%	线性增长
79抽	100%	硬保底
4星角色概率
保底区间	概率	说明
1-9抽	6%	基础概率
10抽	100%	硬保底
保底机制
5星保底: 当获得5星时，有50%概率为限定角色

小保底: 如果不是限定角色，下次5星必为限定角色

4星保底: 每10抽必得4星或以上物品

API参考
主要类：GachaSimulator
方法
__init__()

初始化模拟器，设置默认卡池

reset()

重置所有状态到初始值

pull() -> Tuple[str, int, int]

执行一次抽卡

返回: (物品名称, 辉光珊瑚数量, 荡漾珊瑚数量)

simulate_pulls(num_pulls: int, show_details: bool = False) -> Dict

模拟多次抽卡

参数:

num_pulls: 抽卡次数

show_details: 是否显示每次抽卡详情

返回包含统计信息的字典

set_banner(featured_5star: str, featured_4stars: List[str])

设置当前卡池信息

参数:

featured_5star: 限定5星角色名

featured_4stars: UP四星角色列表

get_pity_info() -> Dict[str, int]

获取当前保底信息

get_character_stats() -> Dict[str, Dict]

获取所有角色统计信息

概率计算函数
rate_5star(rate_number: int) -> float

计算指定保底计数下的5星概率

rate_4star(rate_number: int) -> float

计算指定保底计数下的4星概率

输出示例
text
=== 650次抽卡完整模拟 ===
总抽数: 650
限定5星 Luno: 3
常驻5星:
  Lingyang: 1
  Verina: 1
4星角色:
  Baizhi: 8
  Aalto: 7
  Taoqi: 6
  Sanhua: 5
  Mortefi: 4
3星武器: 616
辉光珊瑚: 210
荡漾珊瑚: 9240
最终保底状态: {'pity_5star': 35, 'pity_4star': 7, 'featured_5star_guaranteed': False}
项目结构
text
gacha_simulator/
├── gacha_simulator.py  # 主模拟器类
├── example_usage.py    # 使用示例
├── README.md          # 项目说明
└── requirements.txt    # 依赖说明
扩展开发
添加新角色
在 reset() 方法中的对应字典添加新角色：

python
self.featured_5stars = {
    # ... 现有角色
    'NewCharacter': [0, 0],  # 添加新角色
}
自定义概率
修改 rate_5star() 和 rate_4star() 方法中的概率计算逻辑。

添加新功能
继承 GachaSimulator 类并添加自定义方法：

python
class EnhancedGachaSimulator(GachaSimulator):
    def multi_pull_analysis(self, total_pulls, num_simulations):
        """多次模拟统计分析"""
        results = []
        for _ in range(num_simulations):
            self.reset()
            result = self.simulate_pulls(total_pulls)
            results.append(result)
        return self.analyze_results(results)
注意事项
此模拟器仅用于教育和娱乐目的

实际游戏概率可能随时间调整，请以游戏官方公告为准

模拟结果仅供参考，不保证与实际游戏体验一致

请合理控制抽卡，享受健康游戏生活

许可证
本项目采用 MIT 许可证 - 详见 LICENSE 文件

贡献
欢迎提交 Issue 和 Pull Request 来改进这个项目！

Fork 本项目

创建特性分支 (git checkout -b feature/AmazingFeature)

提交更改 (git commit -m 'Add some AmazingFeature')

推送到分支 (git push origin feature/AmazingFeature)

开启 Pull Request

更新日志
v1.0.0
初始版本发布

实现基本抽卡机制

添加保底系统和概率计算

提供完整的统计功能

免责声明: 本项目与《鸣潮》官方无关，是粉丝制作的模拟器。所有游戏内容版权归其各自所有者所有。

健康游戏忠告: 抵制不良游戏，拒绝盗版游戏。注意自我保护，谨防受骗上当。适度游戏益脑，沉迷游戏伤身。合理安排时间，享受健康生活。
