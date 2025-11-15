"""
Gerenciamento de histórico de interações
Armazena as últimas 90 interações
"""
import json
import os
from typing import List, Dict, Optional
from datetime import datetime
import config

class HistoryManager:
    """Gerencia o histórico de interações"""
    
    def __init__(self):
        self.history_file = config.Config.HISTORY_FILE
        self.max_history = config.Config.MAX_HISTORY
    
    def _load_history(self) -> List[Dict]:
        """Carrega o histórico do arquivo"""
        if not os.path.exists(self.history_file):
            return []
        
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def _save_history(self, history: List[Dict]):
        """Salva o histórico no arquivo"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao salvar histórico: {e}")
    
    def add_interaction(
        self,
        interaction_id: str,
        messages: List[Dict],
        provider: str,
        model_type: str,
        title: str
    ):
        """Adiciona uma nova interação ao histórico"""
        history = self._load_history()
        
        interaction = {
            "id": interaction_id,
            "messages": messages,
            "provider": provider,
            "model_type": model_type,
            "title": title,
            "timestamp": datetime.now().isoformat()
        }
        
        # Remove interação existente se houver (para atualizar)
        history = [h for h in history if h["id"] != interaction_id]
        
        # Adiciona no início
        history.insert(0, interaction)
        
        # Mantém apenas as últimas MAX_HISTORY interações
        history = history[:self.max_history]
        
        self._save_history(history)
    
    def get_history(self) -> List[Dict]:
        """Retorna todo o histórico"""
        return self._load_history()
    
    def get_interaction(self, interaction_id: str) -> Optional[Dict]:
        """Retorna uma interação específica"""
        history = self._load_history()
        for interaction in history:
            if interaction["id"] == interaction_id:
                return interaction
        return None
    
    def clear_history(self):
        """Limpa todo o histórico"""
        self._save_history([])

