import google.generativeai as genai
from config import Config
import logging
import time
import random

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PostOptimizer:
    """Agente para otimização de descrições de posts usando Google Gemini"""
    
    def __init__(self):
        """Inicializa o agente com as configurações do Gemini"""
        if not Config.GEMINI_API_KEY:
            raise ValueError("Chave da API do Gemini não encontrada. Configure GEMINI_API_KEY no arquivo .env")
        
        # Configurar o Gemini
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
        
        logger.info("Agente de otimização de posts inicializado com sucesso")
    
    def optimize_post(self, original_description: str, platform: str = 'instagram', 
                     additional_context: str = "") -> dict:
        """
        Otimiza a descrição de um post para maior engajamento
        
        Args:
            original_description: Descrição original do post
            platform: Plataforma de destino (instagram, linkedin, twitter)
            additional_context: Contexto adicional (público-alvo, objetivo, etc.)
        
        Returns:
            dict: Resultado da otimização com descrição otimizada e métricas
        """
        try:
            # Validar plataforma
            if platform not in Config.PROMPTS:
                raise ValueError(f"Plataforma não suportada: {platform}. Use: {list(Config.PROMPTS.keys())}")
            
            # Construir prompt
            base_prompt = Config.PROMPTS[platform].format(
                original_description=original_description
            )
            
            # Adicionar contexto se fornecido
            if additional_context:
                base_prompt += f"\n\nContexto adicional: {additional_context}"
            
            # Gerar resposta otimizada com retry automático
            max_retries = 3
            base_delay = 6  # 6 segundos base (10 req/min = 1 req a cada 6 segundos)
            
            for attempt in range(max_retries):
                try:
                    response = self.model.generate_content(
                        base_prompt,
                        generation_config=genai.types.GenerationConfig(
                            temperature=Config.TEMPERATURE,
                            max_output_tokens=Config.MAX_TOKENS
                        )
                    )
                    break  # Sucesso, sair do loop
                    
                except Exception as e:
                    error_msg = str(e)
                    if "429" in error_msg and attempt < max_retries - 1:
                        # Erro de quota, aguardar e tentar novamente
                        if "GenerateRequestsPerMinute" in error_msg:
                            wait_time = base_delay + random.randint(2, 5)  # 6-11 segundos
                        elif "GenerateRequestsPerDay" in error_msg:
                            wait_time = 3600  # 1 hora
                        else:
                            wait_time = base_delay * 2 + random.randint(5, 15)  # 17-27 segundos
                        
                        logger.warning(f"Limite de quota atingido. Aguardando {wait_time} segundos antes da tentativa {attempt + 2}...")
                        time.sleep(wait_time)
                        continue
                    else:
                        # Outro erro ou última tentativa, re-raise
                        raise e
            
            optimized_description = response.text.strip()
            
            # Calcular métricas básicas
            metrics = self._calculate_metrics(original_description, optimized_description)
            
            return {
                'success': True,
                'original_description': original_description,
                'optimized_description': optimized_description,
                'platform': platform,
                'metrics': metrics,
                'suggestions': self._generate_suggestions(optimized_description, platform)
            }
            
        except Exception as e:
            logger.error(f"Erro ao otimizar post: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'original_description': original_description
            }
    
    def _calculate_metrics(self, original: str, optimized: str) -> dict:
        """Calcula métricas básicas para comparar as descrições"""
        return {
            'original_length': len(original),
            'optimized_length': len(optimized),
            'length_change': len(optimized) - len(original),
            'hashtag_count': optimized.count('#'),
            'emoji_count': sum(1 for char in optimized if ord(char) > 127),
            'question_count': optimized.count('?'),
            'exclamation_count': optimized.count('!')
        }
    
    def _generate_suggestions(self, description: str, platform: str) -> list:
        """Gera sugestões adicionais para melhorar o engajamento"""
        suggestions = []
        
        if platform == 'instagram':
            if description.count('#') < 3:
                suggestions.append("Considere adicionar mais hashtags relevantes")
            if description.count('?') == 0:
                suggestions.append("Adicione uma pergunta para gerar mais comentários")
            if description.count('!') == 0:
                suggestions.append("Use exclamações para criar mais entusiasmo")
        
        elif platform == 'linkedin':
            if len(description) < 100:
                suggestions.append("Posts mais longos tendem a ter melhor engajamento no LinkedIn")
            if description.count('?') == 0:
                suggestions.append("Termine com uma pergunta para gerar discussão")
        
        elif platform == 'twitter':
            if len(description) > 200:
                suggestions.append("Considere dividir em threads para posts mais longos")
            if description.count('#') < 2:
                suggestions.append("Adicione hashtags relevantes para aumentar a visibilidade")
        
        return suggestions
    
    def batch_optimize(self, posts: list) -> list:
        """
        Otimiza múltiplos posts de uma vez
        
        Args:
            posts: Lista de dicionários com 'description', 'platform' e 'context'
        
        Returns:
            list: Lista de resultados otimizados
        """
        results = []
        for post in posts:
            result = self.optimize_post(
                original_description=post['description'],
                platform=post.get('platform', 'instagram'),
                additional_context=post.get('context', '')
            )
            results.append(result)
        
        return results 