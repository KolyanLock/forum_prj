from collections import OrderedDict

from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from api.models import Checkbox
from api.serializers import CheckboxSerializer


class CheckboxAPITestCase(APITestCase):

    def test_get(self):
        checkbox_1 = Checkbox.objects.create(name='checkbox_1')
        checkbox_2 = Checkbox.objects.create(name='checkbox_2')
        checkbox_3 = Checkbox.objects.create(name='checkbox_3')
        url = reverse('checkbox-list')
        response = self.client.get(url)
        data = CheckboxSerializer([checkbox_1, checkbox_2, checkbox_3], many=True).data
        self.assertEqual(response.data['results'], data)

    def test_create(self):
        checkbox_1 = {
            "name": "checkbox_1"
        }
        url = reverse('checkbox-list')
        response = self.client.post(url, checkbox_1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = CheckboxSerializer(Checkbox.objects.get(name='checkbox_1')).data
        self.assertEqual(response.data, data)

    def test_update(self):
        Checkbox.objects.create(name='checkbox_1')
        pk = Checkbox.objects.get(name='checkbox_1').pk
        data = {
            "name": "checkbox_1.1",
            "is_checked": False
        }
        url = reverse('checkbox-detail', kwargs={'pk': pk})
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': pk, 'name': 'checkbox_1.1', 'is_checked': False})

    def test_delete(self):
        Checkbox.objects.create(name='checkbox_1')
        pk = Checkbox.objects.get(name='checkbox_1').pk
        url = reverse('checkbox-detail', kwargs={'pk': pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Checkbox.objects.filter(pk=pk))
