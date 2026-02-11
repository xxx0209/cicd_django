from django.shortcuts import render

def fruit(request): # 과일 1개 보여 주기
    bean = {
        "id": "banana",
        "name": "바나나",
        "price": 1000
    }
    return render(request, 'minitest/fruit.html', {'fruit': bean})



def fruit_list(request): # 과일 여러개 보여 주기
    fruit_list = [
        {"id": "apple", "name": "사과", "price": 1000},
        {"id": "pear", "name": "나주배", "price": 2000},
        {"id": "grape", "name": "포도", "price": 3000},
    ]
    return render(request, 'minitest/fruit_list.html', {'fruit_list': fruit_list})
