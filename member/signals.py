from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile

# ============================================================
# 파일 상단 설명
# ============================================================
# 이 파일은 Django의 signal(receiver)들을 정의합니다.
# - post_save 시그널: 모델 인스턴스가 save() 될 때마다 발생
# - @receiver 데코레이터로 시그널과 리스너(함수)를 연결합니다.
#
# 여기서는 User 모델과 연결된 두 개의 리스너를 정의합니다:
# 1) create_user_profile: User가 새로 생성(created=True)될 때 Profile을 자동 생성
# 2) save_user_profile: User가 저장될 때마다 연결된 Profile도 같이 저장
#
# 주의:
# - signals 모듈은 apps.py의 AppConfig.ready()에서 임포트되어야
#   (서버 시작 시 한 번만) 등록/실행되도록 하는 것이 안전합니다.
# - instance.profile 접근 시 Profile이 없으면 AttributeError가 발생할 수 있으므로
#   안전한 접근/예외처리가 필요합니다.
# ============================================================


# ============================================================
# User 생성 시 Profile 자동 생성 리스너
# ============================================================
# @receiver(post_save, sender=User)
#  - post_save: 모델 저장이 완료된 이후에 보내지는 신호(signal)
#  - sender=User: 이 리스너는 User 모델에서 발생하는 post_save 이벤트만 처리
#
# def create_user_profile(sender, instance, created, **kwargs):
#  - sender: 시그널을 보낸 모델 클래스 (여기서는 User 클래스)
#  - instance: 저장된 모델 인스턴스 (여기서는 방금 생성/저장된 User 객체)
#  - created: boolean, 새로 생성된 경우 True (즉 save()가 create 동작이었는지 여부)
#  - **kwargs: 추가 메타 정보 (예: raw, using 등) — 필요하면 사용 가능
#
# 동작:
#  - 새 User 가 생성(created==True)되었을 때만 Profile을 생성합니다.
#  - 이렇게 하면 회원가입(또는 User.objects.create()) 시 자동으로 Profile이 생깁니다.
#
# 왜 필요한가?
#  - User만 생성되고 Profile이 없으면 템플릿이나 코드에서 instance.profile 으로 접근 시 오류 가능.
#  - 자동 생성을 하면 별도 프로필 생성 코드를 매번 호출할 필요가 없어 편리.
#
# 주의/개선점:
#  - Profile.objects.create(user=instance) 호출 시 중복 생성 방지를 위해
#    이미 존재하는 경우를 고려하거나 get_or_create 를 사용해도 좋음.
# ============================================================
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    User 인스턴스가 처음 생성될 때(Profile이 없다면) 자동으로 Profile을 생성.
    - sender: User 클래스
    - instance: 생성된 User 객체
    - created: True이면 새로 생성된 경우
    """
    if created:
        # 새로 생성된 User에 대한 Profile을 생성
        # Profile.objects.create(user=instance) 는 간단하지만,
        # race condition(경쟁 조건)이나 이미 Profile이 존재하는 경우를
        # 완벽히 방어하지 못할 수 있음.
        Profile.objects.create(user=instance)


# ============================================================
# User 저장 시 Profile도 같이 저장하는 리스너
# ============================================================
# @receiver(post_save, sender=User)
#  - 동일하게 User의 post_save 이벤트에 연결된 또 다른 리스너입니다.
#
# def save_user_profile(sender, instance, **kwargs):
#  - created 파라미터는 사용하지 않음(생성 여부에 상관없이 매번 실행)
#  - instance.profile.save(): User가 저장될 때 연결된 Profile을 강제로 저장
#
# 동작:
#  - 예를 들어 User 모델의 필드(예: first_name)를 변경 후 save() 하면,
#    연결된 Profile이 있으면 Profile의 save()도 호출되어 Profile과 연관된 후처리(신호 등)가 실행됩니다.
#
# 주의:
#  - instance.profile 접근 시 Profile이 없으면 AttributeError 발생.
#    따라서 instance.profile이 항상 존재한다고 가정하면 안전하지 않을 수 있음.
#  - create_user_profile가 신뢰성 있게 실행되어 Profile이 항상 만들어진다는 전제 하에만 사용하세요.
#  - 더 안전한 구현: hasattr(instance, 'profile') 체크, try/except 또는 get_or_create 사용.
# ============================================================
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    User가 저장될 때 연결된 Profile도 같이 저장하려는 목적의 리스너.
    - instance.profile.save() 를 호출함으로써 Profile의 save() 로직(예: 자동 이미지 리사이즈 등)이 실행됨.
    - 단, Profile이 없으면 예외가 발생하므로 실제 운영에서는 안전장치가 필요.
    """
    instance.profile.save()