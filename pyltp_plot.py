import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.patches import FancyArrowPatch
import collections
rcParams['font.family'] = ['Yahei Consolas Hybrid', 'Verdana']

WORD_GAP = 0.2
INDENT_LEFT = 0.05
WORD_Y = 0.3
POS_Y = 0.2
ARC_Y = 0.33
RELATION_BACKGROUND_STYLE = {'boxstyle':'square,pad=0', 'fc':'white', 'ec':'none'}

ARC_STYLE={'arrowstyle':"Simple,tail_width=0.5,head_width=4,head_length=8", 'color':"k"}

class PyltpPloter:
    def __init__(self):
        pass

    def plot_it(self, words, postags, nes, deps):
        # words和postags里有Root
        self.words = ['Root'] + words
        self.postags = [''] + postags
        self.nes = nes
        self.deps = deps
        self.__words = []

        fig, ax = plt.subplots()
        inv = ax.transData.inverted()
        fig.canvas.draw()
        # 有些数据必须在渲染的过程中获取，比如一个词在画布上的长度，必须渲染出来
        # 渲染词
        start_x = INDENT_LEFT
        for i in range(len(self.words)):
            the_word_dict = {}
            the_word_dict['x'] = start_x
            word_text = self.words[i]
            the_word_dict['word'] = word_text
            the_text = ax.text(start_x, WORD_Y, word_text)
            renderer = ax.get_renderer_cache()
            position_data = inv.transform(the_text.get_window_extent(renderer))
            the_text_width = position_data[1][0] - position_data[0][0]
            the_word_dict['arc_x'] = start_x + the_text_width / 2
            start_x = start_x + the_text_width + WORD_GAP
            self.__words.append(the_word_dict)
        ax.set_xlim(0, start_x - WORD_GAP + INDENT_LEFT)

        # 渲染词性
        for i in range(len(self.postags)):
            ax.text(self.__words[i]['arc_x'], POS_Y, self.postags[i], horizontalalignment='center')

        # 渲染依存关系
        y_lim = 0
        for i in range(len(self.deps)):
            from_index = i + 1
            to_index = self.deps[i].head
            start_point = [self.__words[from_index]['arc_x'], ARC_Y]
            end_point = [self.__words[to_index]['arc_x'], ARC_Y]
            rad = 0.5 if end_point[0] - start_point[0] > 0 else -0.5
            the_arc = FancyArrowPatch(end_point, start_point, connectionstyle="arc3,rad=%f" % rad, **ARC_STYLE)
            the_arc = ax.add_patch(the_arc)
            position_data = the_arc.get_path().get_extents(transform=None)
            dep_relation_x = position_data.x0 + (position_data.x1 - position_data.x0) / 2
            dep_relation_y = position_data.y0 + (position_data.y1 - position_data.y0) / 2
            y_lim = dep_relation_y if y_lim<dep_relation_y else y_lim
            ax.text(
                dep_relation_x,
                dep_relation_y,
                self.deps[i].relation,
                bbox=RELATION_BACKGROUND_STYLE,
                horizontalalignment='center',
                verticalalignment='center')
        # ax.set_ylim(0,y_lim+POS_Y)
        ax.axis('off')
        
        plt.show()


def main():
    words = ['苹果', '多少', '钱']
    postags = ['n', 'r', 'n']
    nes = []
    Dep = collections.namedtuple('Dep', ['head', 'relation'])
    deps = [Dep(3, 'ATT'), Dep(3, 'ATT'), Dep(0, 'HED')]
    ploter = PyltpPloter()
    ploter.plot_it(words, postags, nes, deps)
    


if __name__ == '__main__':
    main()
