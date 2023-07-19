from rest_framework import serializers

from fitness_food.products.models import Brand, Category, Packaging, Product


class BrandModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            'id',
            'name',
        ]


class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
        ]


class PackagingModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Packaging
        fields = [
            'id',
            'name',
        ]


class ProductModelSerializer(serializers.ModelSerializer):
    image_url = serializers.URLField(read_only=True, allow_null=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'code',
            'barcode',
            'product_name',
            'quantity',
            'categories',
            'packaging',
            'brands',
            'url',
            'image_url',
            'imported_t',
            'status',
        ]
        read_only_fields = [
            'code',
            'image_url',
            'imported_t',
            'status',
        ]

    def to_representation(self, instance: Product) -> dict:
        data = super().to_representation(instance)
        data['brands'] = BrandModelSerializer(
            instance.brands.all(), many=True
        ).data
        data['categories'] = CategoryModelSerializer(
            instance.categories.all(), many=True
        ).data
        data['packaging'] = PackagingModelSerializer(
            instance.packaging.all(), many=True
        ).data
        return data
