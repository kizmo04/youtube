from django.db import models

from youtube import settings


class Video(models.Model):
    title = models.CharField(max_length=200)
    youtube_video_id = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=500)
    is_bookmarked = models.BooleanField(default=False)

    def __str__(self):
        return 'Video id:[{}], title[{}]'.format(self.id, self.title)


# 중간자모델
class VideoBookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    video = models.ForeignKey('video.Video')
    bookmarked_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('user', 'video'),
        )

    def __str__(self):
        return 'Video id[{}], Bookmarked[{}], by User[{}]'.format(
            self.video_id,
            self.id,
            self.user_id,
        )
