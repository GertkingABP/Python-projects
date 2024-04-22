import os
from PIL import Image
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
from time import *
import threading
from queue import Queue

def small_image_mult(image_path): #c процессами и пулами
    try:
        with Image.open(image_path) as im:
            im_resized = im.resize(target_size)
            output_path = os.path.join(output_dir, os.path.basename(image_path))
            im_resized.save(output_path)
            #print(f"Изображение {image_path} успешно обработано и сохранено в {output_path}")
    except Exception as e:
        print(f"Не удалось обработать изображение {image_path}: {e}")

def small_image_thr(q): #c обычными потоками
    while True:
        image_path = q.get()
        if image_path is None:
            break
        try:
            with Image.open(image_path) as im:
                im_resized = im.resize(target_size)
                output_path = os.path.join(output_dir, os.path.basename(image_path))
                im_resized.save(output_path)
                #print(f"Изображение {image_path} успешно обработано и сохранено в {output_path}")
        except Exception as e:
            print(f"Не удалось обработать изображение {image_path}: {e}")
        q.task_done()

input_dir = "input"
output_dir = "output"
target_size = (800, 600)
num = 1

if __name__ == '__main__':
    input_pictures = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.jpg')]
    t = 1
    while t <= 10:
        print(f"\n---------------------------------------------------\nИтерация {t}")
        while num <= 16:
            start_time = time()
            with Pool(processes=num) as pool:
                pool.map(small_image_mult, input_pictures)
            end_time = time()
            print(f"\nВремя вычислений в {num} процесс(е/ах): {end_time - start_time}")
            start_time = 0
            end_time = 0

            start_time = time()
            q = Queue()
            threads = [threading.Thread(target=small_image_thr, args=(q,)) for _ in range(num)]

            for thread in threads:
                thread.start()

            for image in input_pictures:
                q.put(image)

            q.join()

            for _ in range(num):
                q.put(None)

            for thread in threads:
                thread.join()

            end_time = time()
            print(f"\nВремя вычислений в {num} поток(е/ах): {end_time - start_time}")

            num += 1
            start_time = 0
            end_time = 0
        t += 1
        num = 1