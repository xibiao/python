import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

class Captcha(object):
    @staticmethod
    def check_code(width=100, height=30, char_num=4, font_file='../static/font/Monaco.ttf', font_size=20):
        """
        生成随机图片验证码，参考：https://www.cnblogs.com/wupeiqi/articles/5812291.html
        :param width: 图片宽度
        :param height: 图片高度
        :param char_num: 图片中字符的个数
        :param font_file: 字体文件
        :param font_size: 字体大小
        :return: 图片验证码(用于在界面展示)和验证码字符(用于校验用户输入的验证码是否正确)
        """
        code = []
        img = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(img, mode='RGB')

        def randomChar():
            """
            生成随机字母
            :return:
            """
            # 生成随机数字
            # return str(random.randint(0, 9))
            return chr(random.randint(65, 90))

        def randomColor():
            """
            生成随机颜色
            :return:
            """
            return (random.randint(0, 255), random.randint(10, 255), random.randint(64, 255))

        # 写文字
        font = ImageFont.truetype(font_file, font_size)
        for i in range(char_num):
            char = randomChar()
            code.append(char)
            h = random.randint(0, 4)
            draw.text((i * width / char_num, h), char, font=font, fill=randomColor())

        # 写干扰点
        for i in range(40):
            draw.point([random.randint(0, width), random.randint(0, height)], fill=randomColor())

        # 写干扰圆圈
        for i in range(30):
            draw.point([random.randint(0, width), random.randint(0, height)], fill=randomColor())
            x = random.randint(0, width)
            y = random.randint(0, height)
            draw.arc((x, y, x + 4, y + 4), 0, 90, fill=randomColor())

        # 画干扰线
        for i in range(4):
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = random.randint(0, width)
            y2 = random.randint(0, height)

            draw.line((x1, y1, x2, y2), fill=randomColor())

        img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
        return img, ''.join(code)


if __name__ == '__main__':
    # 1. 直接打开
    # img,code = check_code()
    # img.show()

    # 2. 写入文件
    img,code = Captcha.check_code(font_file='../static/font/Monaco.ttf')
    print("code===", code)
    with open('../static/img/code.png','wb') as f:
        img.save(f,format='png')

    # 3. 写入内存(Python3)
    # from io import BytesIO
    # stream = BytesIO()
    # img.save(stream, 'png')
    # stream.getvalue()

    # 4. 写入内存（Python2）
    # import StringIO
    # stream = StringIO.StringIO()
    # img.save(stream, 'png')
    # stream.getvalue()
