from django.contrib.auth.models import User
from .models import Achievement, UserAchievement

class AchievementChecker:
    @staticmethod
    def check_achievements(user):
        # Получаем все возможные достижения
        achievements = Achievement.objects.all()
        
        # Получаем уже полученные достижения пользователя
        user_achievements = UserAchievement.objects.filter(user=user)
        achieved_ids = [ua.achievement.id for ua in user_achievements]
        
        new_achievements = []
        
        for achievement in achievements:
            if achievement.id in achieved_ids:
                continue
                
            # Проверяем условие получения достижения
            condition_met = False
            try:
                # Пример условия: "lessons_completed=5"
                field, value = achievement.condition.split('=')
                value = int(value)
                
                if field == 'lessons_completed':
                    condition_met = user.profile.lessons_completed >= value
                elif field == 'topics_completed':
                    condition_met = user.profile.topics_completed >= value
                elif field == 'login_streak':
                    condition_met = user.profile.login_streak >= value
                # Добавьте другие условия по необходимости
                
            except (ValueError, AttributeError):
                pass
                
            if condition_met:
                # Создаем запись о получении достижения
                UserAchievement.objects.create(
                    user=user,
                    achievement=achievement
                )
                new_achievements.append(achievement)
                
        return new_achievements