import random
import matplotlib.pyplot as plt
import numpy as np


class GachaSimulator:
    def __init__(self):
        """
        定义所有实例属性并初始化
        """
        # 五星限定角色是否保底
        self.featured_5star_guaranteed = False
        # 距上个五星的抽数
        self.pity_5star = 0
        # 常驻池五星角色及已有数、抽到数：'角色名': [链数, 抽到]
        self.standard_5stars = {}
        # 限定池五星角色及已有数、抽到数：'角色名': [链数, 抽到]
        self.featured_5stars = {}
        # 本期概率up的限定五星角色
        self.rate_up_5star = ''
        # 距上个四星的抽数
        self.pity_4star = 0
        # 四星角色及已有数、抽到数：'角色名': [链数, 抽到]
        self._4stars = {}
        # 本期概率up的四星角色
        self.rate_up_4stars = []
        # 抽取的三星武器数量
        self.weapon = 0
        # 本次抽取事件中获取的余波珊瑚（大珊瑚）
        self.total_afterglow_coral_count = 0
        # 本次抽取事件中获取的残振珊瑚（小珊瑚）
        self.total_oscillated_coral_count = 0
        # 总抽数
        self.pull_count = 0
        # 抽卡历史
        self.pull_history = []

        # 调用reset方法初始化
        self.reset()

    def reset(self):
        """
        重置所有状态到初始值
        """
        self.featured_5star_guaranteed = False
        self.pity_5star = 0
        self.standard_5stars = {
            '凌阳': [-1, 0],
            '安可': [-1, 0],
            '卡卡罗': [-1, 0],
            '鉴心': [-1, 0],
            '维里奈': [-1, 0],
        }
        self.featured_5stars = {
            '折枝': [-1, 0],
            '珂莱塔': [-1, 0],
            '长离': [-1, 0],
            '布兰特': [-1, 0],
            '露帕': [-1, 0],
            '吟霖': [-1, 0],
            '相里要': [-1, 0],
            '奥古斯特': [-1, 0],
            '忌炎': [-1, 0],
            '夏空': [-1, 0],
            '卡提希娅': [-1, 0],
            '尤诺': [-1, 0],
            '今汐': [-1, 0],
            '守岸人': [-1, 0],
            '菲比': [-1, 0],
            '赞妮': [-1, 0],
            '椿': [-1, 0],
            '洛可可': [-1, 0],
            '坎特蕾拉': [-1, 0],
            '弗洛洛': [-1, 0],
        }
        self.rate_up_5star = '尤诺'
        self.pity_4star = 0
        self._4stars = {
            '散华': [-1, 0],
            '白芷': [-1, 0],
            '釉瑚': [-1, 0],
            '炽霞': [-1, 0],
            '莫特斐': [-1, 0],
            '渊武': [-1, 0],
            '灯灯': [-1, 0],
            '泱泱': [-1, 0],
            '秋水': [-1, 0],
            '桃祈': [-1, 0],
            '丹瑾': [-1, 0],
        }
        self.rate_up_4stars = ['白芷', '秋水', '桃祈']
        self.total_afterglow_coral_count = 0
        self.total_oscillated_coral_count = 0

    @staticmethod
    def rate_5star(rate_number: int):
        """
        计算当前抽卡的五星概率
        参数：
            rate_number: 距上个五星为第几抽
        返回：
            float: 本次抽到五星的概率
        """
        # 概率
        local_rate = 0
        if rate_number < 66:
            local_rate = 0.008
        elif rate_number < 71:
            local_rate = 0.008 + 0.04*(rate_number - 65)
        elif rate_number < 76:
            local_rate = 0.208 + 0.08*(rate_number - 70)
        elif rate_number < 79:
            local_rate = 0.608 + 0.1*(rate_number - 75)
        elif rate_number == 79:
            local_rate = 1
        else:
            print(f'五星保底计数错误：{rate_number}，应小于或等于79！')
        return local_rate

    @staticmethod
    def rate_4star(rate_number: int):
        """
        计算当前抽卡的四星概率
        参数：
            rate_number: 距上个四星为第几抽
        返回：
            float: 本次抽到四星的概率
        """
        # 概率
        local_rate = 0
        if rate_number < 10:
            local_rate = 0.06
        elif rate_number == 10:
            local_rate = 1
        else:
            print(f'四星保底计数错误：{rate_number}，应小于或等于10！')
        return local_rate

    def pull(self):
        """
        执行一次抽卡
        返回：
            tuple[str, int, int]
            --抽取到的角色或武器
            --本次抽取获得的余波珊瑚（大珊瑚）
            --本次抽取获取的残振珊瑚（小珊瑚）
        """
        # 本次抽到的角色或武器
        local_item = ''
        # 本次抽取获得的余波珊瑚（大珊瑚）
        local_obtained_afterglow_coral = 0
        # 本次抽取获取的残振珊瑚（小珊瑚）
        local_obtained_oscillated_coral = 0

        # 用于对抽取物判断的随机浮点数，区间[0, 1)
        local_random = random.random()

        # 检查是否抽到五星角色
        if self.rate_5star(self.pity_5star + 1) > local_random:
            # 抽到五星，重置五星角色保底计数
            self.pity_5star = 0

            # 如果本次同时满足四星角色保底，重置四星角色保底计数
            if self.pity_4star == 9:
                self.pity_4star = 0

            # 检查抽到的是常驻五星还是限定五星角色
            if not self.featured_5star_guaranteed and random.random() < 0.5:
                # 抽到常驻五星角色
                # 设置大保底，下次五星必定为本期限定五星角色
                self.featured_5star_guaranteed = True
                # 判断抽取到的常驻五星角色
                local_item = random.choice(list(self.standard_5stars.keys()))

                # 更新常驻五星角色拥有情况和抽到数，计算本次获取的珊瑚
                if self.standard_5stars[local_item][0] < 6:
                    # 常驻五星角色未满链，链数和抽到数+1、获得45余波珊瑚（大珊瑚）
                    self.standard_5stars[local_item][0] += 1
                    self.standard_5stars[local_item][1] += 1
                    local_obtained_afterglow_coral = 45
                else:
                    # 常驻五星角色已满链，链数不变，抽到数+1、获得70余波珊瑚（大珊瑚）
                    self.standard_5stars[local_item][1] += 1
                    local_obtained_afterglow_coral = 70
            else:
                # 抽到限定五星角色，
                # 重置大保底
                self.featured_5star_guaranteed = False
                local_item = self.rate_up_5star

                # 更新限定五星角色拥有情况和抽到数，计算本次获取的珊瑚
                if self.featured_5stars[local_item][0] < 7:
                    # 限定五星角色未满链，链数和抽到数+1、获得15余波珊瑚（大珊瑚）
                    self.featured_5stars[local_item][0] += 1
                    self.featured_5stars[local_item][1] += 1
                    local_obtained_afterglow_coral = 15
                else:
                    # 限定五星角色已满链，链数不变，抽到数+1、获得40余波珊瑚（大珊瑚）
                    self.featured_5stars[local_item][1] += 1
                    local_obtained_afterglow_coral = 40

        # 检查是否抽到四星角色
        elif self.rate_4star(self.pity_4star + 1) > local_random:
            # 抽到四星角色，重置四星角色保底计数
            self.pity_4star = 0
            # 五星角色保底计数+1
            self.pity_5star += 1

            # 检查抽到的是概率up四星还是非概率up四星角色
            if random.random() < 0.5:
                # 抽到非概率up四星角色
                # 创建非概率up四星角色列表
                local_non_rate_up_4stars = [c for c in self._4stars if c not in self.rate_up_4stars]
                # 判断抽取到的非概率up四星角色
                local_item = random.choice(local_non_rate_up_4stars)
            else:
                # 抽到概率up四星角色
                # 判断抽取到的概率up四星角色
                local_item = random.choice(self.rate_up_4stars)

            # 更新四星角色拥有情况和抽到数，计算本次获取的珊瑚
            if self._4stars[local_item][0] < 6:
                # 四星角色未满链，链数和抽到数+1、获得3余波珊瑚（大珊瑚）
                self._4stars[local_item][0] += 1
                self._4stars[local_item][1] += 1
                local_obtained_afterglow_coral = 3
            else:
                # 四星角色已满链，链数不变，抽到数+1、获得8余波珊瑚（大珊瑚）
                self._4stars[local_item][1] += 1
                local_obtained_afterglow_coral = 8

        # 既没抽到五星角色，也没抽到四星角色，则抽取到三星武器
        else:
            # 四星和五星角色保底计数+1
            self.pity_4star += 1
            self.pity_5star += 1
            local_item = '3星武器'
            # 三星武器计数+1
            self.weapon += 1

            # 抽到三星武器，获得15残振珊瑚（小珊瑚）
            local_obtained_oscillated_coral = 15

        return local_item, local_obtained_afterglow_coral, local_obtained_oscillated_coral

    def simulate_pulls(self, num_pulls: int, verbose: bool = False):
        """
        模拟多次抽卡
        参数：
            num_pulls: 抽卡次数
            verbose: 是否显示每次抽卡结果
        """
        # 执行指定次数抽卡
        for pull in range(num_pulls):
            # 总抽数更新
            self.pull_count += 1
            # 执行一次抽卡，获得抽取物、珊瑚
            local_item, local_obtained_afterglow_coral, local_obtained_oscillated_coral = self.pull()
            self.total_afterglow_coral_count += local_obtained_afterglow_coral
            self.total_oscillated_coral_count += local_obtained_oscillated_coral

            if verbose:
                # verbose为True，输出抽卡结果
                if local_obtained_afterglow_coral > 8:
                    print(f'第{self.pull_count}抽：获得\033[33m{local_item:-^10}\033[0m和'
                          f'{local_obtained_afterglow_coral}余波珊瑚。')
                elif local_obtained_afterglow_coral > 0:
                    print(f'第{self.pull_count}抽：获得\033[35m{local_item:-^10}\033[0m和'
                          f'{local_obtained_afterglow_coral}余波珊瑚。')
                elif local_obtained_oscillated_coral > 0:
                    print(f'第{self.pull_count}抽：获得{local_item:-^10}和{local_obtained_oscillated_coral}残振珊瑚。')
                else:
                    # 正常情况下此种情况不存在
                    print(f'第{self.pull_count}抽：获得{local_item:-^10}。')

            self.pull_history.append({
                'pull_number': pull + 1,
                'item': local_item,
                'afterglow_coral': local_obtained_afterglow_coral,
                'oscillated_coral': local_obtained_oscillated_coral,
            })

    def get_pity_info(self):
        """
        获取当前保底信息
        返回：
            dict: 包含保底抽数信息的字典
        """
        return {
            'pity_5star': self.pity_5star,
            'pity_4star': self.pity_4star,
            'featured_5star_guaranteed': self.featured_5star_guaranteed
        }

    def get_character_stats(self):
        """
        获取所有角色统计信息
        返回：
            dict: 包含角色统计信息的字典
        """
        stats = {
            'featured_5star': {},
            'standard_5stars': {},
            'star_4s': {},
        }

        # 限定五星统计
        for char, (owned, obtained) in self.featured_5stars.items():
            if obtained > 0:
                stats['featured_5star'][char] = {
                    'owned': owned,
                    'obtained': obtained,
                }

        # 常驻五星统计
        for char, (owned, obtained) in self.standard_5stars.items():
            if obtained > 0:
                stats['standard_5stars'][char] = {
                    'owned': owned,
                    'obtained': obtained
                }

        # 四星统计
        for char, (owned, obtained) in self._4stars.items():
            if obtained > 0:
                stats['star_4s'][char] = {
                    'owned': owned,
                    'obtained': obtained
                }

        return stats

    def set_banner(self, featured_5star: str, featured_4stars: list):
        """
        设置当前卡池概率up角色
        参数:
            featured_5star: 限定5星角色名
            featured_4stars: UP四星角色列表
        """
        self.rate_up_5star = featured_5star
        self.rate_up_4stars = featured_4stars.copy()

        # 确保限定5星在字典中，否则将其加入角色池
        if featured_5star not in self.featured_5stars:
            self.featured_5stars[featured_5star] = [-1, 0]

        # 确保UP四星在字典中，否则将其加入角色池
        for char in featured_4stars:
            if char not in self._4stars:
                self._4stars[char] = [-1, 0]


if __name__ == '__main__':
    # 模拟次数
    n = 2000000
    # 最终抽数统计
    pulls_count_list = []

    for i in range(n):
        # 创建抽卡模拟器实例
        simulator = GachaSimulator()
        # 抽卡直到获得满链限定角色，余波珊瑚可换取共鸣链
        while True:
            simulator.simulate_pulls(1, False)
            if simulator.featured_5stars[simulator.rate_up_5star][0] == 4 and simulator.total_afterglow_coral_count > 720:
                pulls_count_list.append(simulator.pull_count)
                break
            elif simulator.featured_5stars[simulator.rate_up_5star][0] == 5 and simulator.total_afterglow_coral_count > 360:
                pulls_count_list.append(simulator.pull_count)
                break
            elif simulator.featured_5stars[simulator.rate_up_5star][0] == 6:
                pulls_count_list.append(simulator.pull_count)
                break
            else:
                continue
    average = sum(pulls_count_list) / len(pulls_count_list)

    values, counts = np.unique(pulls_count_list, return_counts=True)
    # 绘制频率分布图
    plt.bar(values, counts)
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    plt.title('Frequency Distribution')
    plt.show()

    print(f'共经过{n}次模拟，获得当期满链限定五星角色所需的抽数期望是{average}（余波珊瑚换取限定角色共鸣链汇入统计）。')

