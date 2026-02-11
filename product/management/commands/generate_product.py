import os
import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from product.models import Product, Category  # 장고 모델

# Django는 아래 규칙을 기반으로 관리 명령을 자동 검색합니다:
# management 폴더가 있어야 함
# 그 안에 commands 폴더가 있어야 함
# 해당 폴더 안에 <명령어>.py 파일이 있어야 함
# 파일 안에는 Command 클래스를 정의해야 함
# 이 네 가지가 정확해야 Django는 이 파일을 “명령어”로 인식합니다.

# python manage.py generate_product 라고 실행하면 이미자가 추가됩니다.

IMAGE_FOLDER = r"C:\shop\images"

class Command(BaseCommand):
    help = 'Generate sample products from images'

    def handle(self, *args, **kwargs):
        products = self.create_all_products()
        Product.objects.bulk_create(products)
        self.stdout.write(self.style.SUCCESS(f'{len(products)} products created.'))

    def get_image_file_names(self):
        image_files = []
        if not os.path.exists(IMAGE_FOLDER) or not os.path.isdir(IMAGE_FOLDER):
            self.stdout.write(self.style.WARNING(f'{IMAGE_FOLDER} 폴더가 존재하지 않습니다'))
            return image_files

        for f in os.listdir(IMAGE_FOLDER):
            if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_files.append(f)
        return image_files

    def create_product(self, image_name):
        lower = image_name.lower()
        # 카테고리 결정
        if any(x in lower for x in ['americano','latte','milk','coffee','cappuccino','juice','wine']):
            category = Category.BEVERAGE
        elif any(x in lower for x in ['croissant','ciabatta','brioche','baguette','scone','pretzel','muffin']):
            category = Category.BREAD
        elif any(x in lower for x in ['cake','macaron','pie','tart']):
            category = Category.CAKE
        else:
            category = Category.ALL

        # 이름 추출
        name = self.format_name_from_image(image_name)

        # 설명 자동 생성
        tastes = ["달콤하고", "고소하고", "부드럽고", "상큼하고", "진한", "담백하고", "촉촉한", "향긋한"]
        features = ["풍미가 느껴져요", "맛이 나요", "향이 가득해요", "식감이 좋아요", "기분이 좋아져요"]
        description = f"{name}는 {random.choice(tastes)} {random.choice(features)}."

        # 가격
        if category == Category.BEVERAGE:
            price = random.randrange(3500, 6001, 100)
        elif category == Category.BREAD:
            price = random.randrange(2000, 5001, 100)
        elif category == Category.CAKE:
            price = random.randrange(5000, 9001, 100)
        else:
            price = 3000

        # 재고
        stock = random.randrange(50, 201, 10)

        # 등록일
        inputdate = date.today() - timedelta(days=random.randint(1,30))

        return Product(
            name=name,
            category=category,
            description=description,
            image=image_name,
            price=price,
            stock=stock,
            inputdate=inputdate
        )

    def format_name_from_image(self, file_name):
        name = os.path.splitext(file_name)[0]
        name = ''.join([c if not c.isdigit() else '' for c in name.replace('_',' ') ]).strip()

        dictionary = {
            "americano": "아메리카노",
            "latte": "바닐라라떼",
            "milk": "우유",
            "coffee": "커피",
            "cappuccino": "카푸치노",
            "juice": "주스",
            "wine": "와인",
            "croissant": "크로아상",
            "ciabatta": "치아바타",
            "brioche": "브리오슈",
            "baguette": "바게트",
            "pretzel": "프레첼",
            "scone": "스콘",
            "focaccia": "포카치아",
            "donut": "도넛",
            "muffin": "머핀",
            "roll": "버터롤",
            "bread": "식빵",
            "bun": "모닝빵",
            "pie": "애플파이",
            "tart": "타르트",
            "cake": "케이크",
            "macaron": "마카롱"
        }

        for key in dictionary:
            if key in name.lower():
                return dictionary[key]
        return name

    def create_all_products(self):
        return [self.create_product(f) for f in self.get_image_file_names()]
