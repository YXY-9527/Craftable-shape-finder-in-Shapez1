import os
import collections

def rotate(shapez):
    '''
    旋转图形的逻辑,每层左移一位
    1234:1234:1234:1234->4123:4123:4123:4123
    '''
    return ((shapez&0xeeee)>>1)|((shapez&0x1111)<<3)

def stack(bottom,top):
    '''
    堆叠图形的逻辑,检测到碰撞再top压在bottom上
     0000:1000:0001:1111
    +1111:0110:0000:0000
    =1111:1110:0001:0000
    '''
    if bottom & top<<12:return bottom
    elif bottom & top<<8:return bottom | (top<<12 & 0xf000)
    elif bottom & top<<4:return bottom | (top<<8 & 0xff00)
    elif bottom & top:return bottom | (top<<4 & 0xfff0)
    else:return bottom | top

def drop(shapez):
    '''
    切割图形下坠逻辑，写麻烦了
    有空行就拆开堆叠
    '''
    if shapez == 0:return 0
    if shapez & 0x0f00 == 0:shapez = stack(shapez & 0x00ff,shapez >> 12)
    if shapez & 0x00f0 == 0:shapez = stack(shapez & 0x000f,shapez >> 8)
    if shapez & 0x000f == 0:shapez = stack(0,shapez >> 4)
    return shapez

def cut(shapez):
    '''
    切割图形逻辑
    分两半后进行下坠判断
    '''
    res1,res2 = shapez&0x3333,shapez&0xcccc
    return drop(res1),drop(res2)

def show(shapez):
    '''
    展示约定俗称的竖状图
    '''
    print('{:0>4b}\n{:0>4b}\n{:0>4b}\n{:0>4b}'.format(shapez>>12,shapez>>8&15,shapez>>4&15,shapez&15))

def count():
    '''
    计数全可制作图形,大概需要10min
    '''
    craftable_shapez = {15}
    processed_shapez = {15}
    queue = collections.deque()
    queue.append(15)
    count = 0
    while(queue):
        shape = queue.pop()
        if shape == 0:
            continue
        count += 1
        new_shapez = set()
        for cshape in craftable_shapez:
            new_shapez.add(stack(shape,cshape))
            new_shapez.add(stack(cshape,shape))
        a,b = cut(shape)
        if a:new_shapez.add(a)
        if b:new_shapez.add(b)
        shape = rotate(shape)
        a,b = cut(shape)
        if a:new_shapez.add(a)
        if b:new_shapez.add(b)
        new_shapez.add(shape)
        shape = rotate(shape)
        new_shapez.add(shape)
        shape = rotate(shape)
        new_shapez.add(shape)

        for new_shape in new_shapez:
            craftable_shapez.add(new_shape)
            if new_shape not in processed_shapez:
                queue.append(new_shape)
                processed_shapez.add(new_shape)
        if count%100 == 0:
            os.system('cls')
            print('Count number:{} Craftable shapes number:{}'.format(count,len(craftable_shapez)))

    os.system('cls')
    print('Count number:{} Craftable shapes number:{}'.format(count,len(craftable_shapez)))
    return craftable_shapez

def save(shapes, filename="shapes.txt"):
    with open(filename, 'w', encoding='utf-8') as f:
        for shape in sorted(shapes):
            s = int(shape)
            f.write('\n{:0>4b}:{:0>4b}:{:0>4b}:{:0>4b}'.format(s>>12,s>>8&15,s>>4&15,s&15)[::-1])
    print(f"形状已保存到 {filename}")

if __name__ == '__main__':
    shapes = count()
    save(shapes)