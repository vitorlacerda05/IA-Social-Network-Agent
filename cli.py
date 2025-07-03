#!/usr/bin/env python3
"""
Interface de linha de comando para o Agente de Otimização de Posts
"""

import argparse
import json
import sys
from post_optimizer import PostOptimizer
from config import Config

def main():
    parser = argparse.ArgumentParser(
        description="Agente de Otimização de Posts - Otimize suas descrições para maior engajamento",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python cli.py -d "Hoje vou falar sobre marketing digital" -p instagram
  python cli.py -d "A importância da liderança" -p linkedin -c "Público: executivos"
  python cli.py -f posts.json
        """
    )
    
    parser.add_argument(
        '-d', '--description',
        help='Descrição original do post'
    )
    
    parser.add_argument(
        '-p', '--platform',
        choices=['instagram', 'linkedin', 'twitter'],
        default='instagram',
        help='Plataforma de destino (padrão: instagram)'
    )
    
    parser.add_argument(
        '-c', '--context',
        default='',
        help='Contexto adicional (público-alvo, objetivo, etc.)'
    )
    
    parser.add_argument(
        '-f', '--file',
        help='Arquivo JSON com múltiplos posts para otimizar'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Arquivo de saída para salvar os resultados (padrão: stdout)'
    )
    
    parser.add_argument(
        '--pretty',
        action='store_true',
        help='Formatação bonita da saída JSON'
    )
    
    args = parser.parse_args()
    
    # Verificar se a API key está configurada
    if not Config.GEMINI_API_KEY:
        print("❌ Erro: Chave da API do Gemini não encontrada!")
        print("Configure GEMINI_API_KEY no arquivo .env")
        print("Obtenha sua chave gratuita em: https://makersuite.google.com/app/apikey")
        sys.exit(1)
    
    try:
        optimizer = PostOptimizer()
        
        if args.file:
            # Modo batch - processar arquivo
            with open(args.file, 'r', encoding='utf-8') as f:
                posts = json.load(f)
            
            print(f"🔄 Processando {len(posts)} posts...")
            results = optimizer.batch_optimize(posts)
            
        elif args.description:
            # Modo single post
            print("🔄 Otimizando post...")
            result = optimizer.optimize_post(
                original_description=args.description,
                platform=args.platform,
                additional_context=args.context
            )
            results = [result]
            
        else:
            print("❌ Erro: Forneça uma descrição (-d) ou arquivo (-f)")
            parser.print_help()
            sys.exit(1)
        
        # Processar resultados
        output_data = []
        for i, result in enumerate(results):
            if result['success']:
                print(f"✅ Post {i+1} otimizado com sucesso!")
                
                # Exibir resultado
                print(f"\n📝 Original: {result['original_description']}")
                print(f"✨ Otimizado: {result['optimized_description']}")
                print(f"📱 Plataforma: {result['platform']}")
                
                # Métricas
                metrics = result['metrics']
                print(f"📊 Métricas:")
                print(f"   - Tamanho: {metrics['original_length']} → {metrics['optimized_length']} chars")
                print(f"   - Hashtags: {metrics['hashtag_count']}")
                print(f"   - Perguntas: {metrics['question_count']}")
                print(f"   - Exclamações: {metrics['exclamation_count']}")
                
                # Sugestões
                if result['suggestions']:
                    print(f"💡 Sugestões:")
                    for suggestion in result['suggestions']:
                        print(f"   - {suggestion}")
                
                output_data.append(result)
                print("-" * 50)
                
            else:
                print(f"❌ Erro no post {i+1}: {result['error']}")
                output_data.append(result)
        
        # Salvar resultado
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2 if args.pretty else None, ensure_ascii=False)
            print(f"💾 Resultados salvos em: {args.output}")
        
        elif args.pretty:
            print("\n📄 Resultado JSON:")
            print(json.dumps(output_data, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 