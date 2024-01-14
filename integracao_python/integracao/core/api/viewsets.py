from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets

from core.models import DataModel
from .serializers import DataModelSerializer
from django.conf import settings
import requests

class DataModelViewSet(viewsets.ModelViewSet):
    import ipdb ; ipdb.set_trace()

    queryset = DataModel.objects.all()
    serializer_class = DataModelSerializer

    def format_data_for_gpt(data):
        description = "Análise de dados de vendas:\n"
        for item in data:
            description += f"Produto: {item['nome']}, Quantidade: {item['quantidade']}, Valor: {item['valor']}, Data: {item['data']}\n"
        description += "Por favor, forneça insights estratégicos sobre como lidar com os produtos e estoque, e proponha ações para melhoria do desempenho de vendas nos próximos meses."
       
        return description

    def send_data_to_gpt(data):
    
        formatted_data = format_data_for_gpt(data)
        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "prompt": formatted_data,
            "max_tokens": 150  # Ajuste conforme necessário
        }
        response = requests.post("https://api.openai.com/v1/engines/davinci/completions", json=payload, headers=headers)
        return response.json()


    @action(detail=False, methods=['post'])
    def analyze_data(self, request):
        data = request.data.get('vendasData', [])
        if not data:
            return Response({'error': 'Nenhum dado fornecido'}, status=400)

        formatted_data = self.format_data_for_gpt(data)
        gpt_response = self.send_data_to_gpt(formatted_data)
        
        return Response(gpt_response)