from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from phone_field import PhoneField
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.
class Userregister(models.Model):
	postuser = models.ForeignKey(User, on_delete=models.CASCADE)
	fullname = models.CharField(max_length=20,null=False)
	phone = PhoneField(blank=True, help_text='Contact phone number',E164_only=False,)
	city = models.CharField(max_length=20,null=False)
	state = models.CharField(max_length=20,null=False)
	location = models.CharField(max_length=20,null=False)
	iteam = models.CharField(max_length=20, null=False)
	landmark = models.CharField(max_length=20, null=False)
	datetime = models.DateTimeField()
	content = models.TextField()
	iteam_pic = models.ImageField(null=False,blank=False)
	def get_absolute_url(self):
		return reverse("detail",kwargs={"id":self.id}) #f"/search/{self.id}/"
	def __str__(self):
		return self.fullname


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username

	def last_seen(self):
		return cache.get('last_seen_%s' % self.user.username)

	def online(self):
		if self.last_seen():
			now = datetime.datetime.now()
			if now > (self.last_seen() + datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT)):
				return False
			else:
				return True
		else:
			return False

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)
