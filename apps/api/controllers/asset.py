from apps.seller.models.asset import Asset
from rest_framework import serializers
from apps.admin.utils.exception_handling import ExceptionHandler

class AssetSerializer(serializers.ModelSerializer):
  peephole_image = serializers.Field(source='image.peephole')

  class Meta:
    model = Asset
    fields = ('name', 'description', 'ilk', 'peephole_image',)
