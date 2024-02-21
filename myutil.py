# Class names
class_names = ['-', '0', '1', '2', '3', '3een', '4', '5', '6', '7', '8', '9', 'alf', 'beh', 'dal', 'fehh', 'gem', 'heh', 'lam', 'mem',
 'noon', 'noonnoon', 'qaf', 'reh', 'sad', 'seen', 'tah', 'waw', 'yeeh', 'yeh']

car_type_dic = {2: 'car',
                3: 'motorbike',
                5: 'bus',
                7: 'truck'}

en_to_ar = {'-': '-',
            '0': '٠',
            '1': '١',
            '2': '٢',
            '3': '٣',
            '3een': 'ع',
            '4': '٤',
            '5': '٥',
            '6': '٦',
            '7': '٧',
            '8': '٨',
            '9': '٩',
            'alf': 'ا',
            'beh': 'ب',
            'dal': 'د',
            'fehh': 'ف',
            'gem': 'ج',
            'heh': 'ه',
            'lam': 'ل',
            'mem': 'م',
            'noon': 'ن',
            'noonnoon': 'ن',
            'qaf': 'ق',
            'reh': 'ر',
            'sad': 'ص',
            'seen': 'س',
            'tah': 'ط',
            'waw': 'و',
            'yeeh': 'ى',
            'yeh': 'ى'}

def sort_bounding_boxes(bounding_boxes):
    sorted_boxes = sorted(bounding_boxes, key=lambda box: box[1][0][0], reverse=True)
    return sorted_boxes

def get_char(mylists):
    nums_and_chars = [box[0] for box in mylists]
    return nums_and_chars
def number_or_char(mylist):
    numbers = []
    chars = []

    for i in mylist:
        if i in ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩']:
            numbers.append(i)
        elif isinstance(i, str) and len(i.strip()) == 1:
            chars.append(i)

    return numbers, chars

def myformat(results):
    points =[]
    for i, r in enumerate(results):
        for index, box in enumerate(r.boxes):
            object_id = int(box.cls.item())
            bbox_data = box.xywh.tolist()
            # Get the class name
            class_name = class_names[object_id]
            class_name = en_to_ar.get(class_name, "Unknown")
            points.append([class_name, bbox_data])
        # print(points)
        sorted_points = sort_bounding_boxes(points)
        nums_and_chars = get_char(sorted_points)

        numbers, chars = number_or_char(nums_and_chars)
        numbers = ' '.join(numbers)
        chars = ' '.join(chars)
        return numbers, chars
